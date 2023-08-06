/*
Copyright 2019-2022 Matthieu Dien and Martin Pépin
Distributed under the license GNU GPL v3 or later
See LICENSE.txt for more informations
*/

#include "cpp_simulator.hpp"
#include "cpp_xoshiro.hpp"
#include <cmath>
#include <iostream>
#include <stack>
#include <stdexcept>
#include <vector>

/* Getters and setters **********************************************/

rule_type CRule::get_type() const { return this->type; }

// REF
int CRule::get_ref_id() const { return this->_as_ref.id; }
void CRule::set_ref_rule(CRule *rule) { this->_as_ref.rule = rule; }
const CRule *CRule::get_ref_rule() const { return this->_as_ref.rule; }

// MARKER
int CRule::get_marker_id() const { return this->_as_marker.id; }

// PRODUCT
const std::vector<CRule *> &CRule::get_product_args() const {
  return *this->_as_product.args;
}

// UNION
const std::vector<CRule *> &CRule::get_union_args() const {
  return *this->_as_union.args;
}
const std::vector<std::vector<double> > &CRule::get_union_weights() const {
  return *this->_as_union.weights;
}

// SET / SEQ / MSET
const CRule *CRule::get_iter_arg() const { return this->_as_iterated_rule.arg; }
const std::vector<double> &CRule::get_iter_weight() const {
  return *this->_as_iterated_rule.weight;
}
const std::vector<double> &CRule::get_iter_arg_weight() const {
  return *this->_as_iterated_rule.arg_weight;
}
int CRule::get_iter_lower_size() const {
  return this->_as_iterated_rule.lower_size;
}
int CRule::get_iter_upper_size() const {
  return this->_as_iterated_rule.upper_size;
}

// MSET only
const std::vector<std::vector<double> > &
CRule::get_mset_partitions_weight() const {
  return *this->_as_iterated_rule.partitions_weight;
}

/* Grammar constructors *********************************************/

CRule *make_ref(int id) {
  CRule *ref = new CRule(rule_type::REF);
  ref->_as_ref.id = id;
  return ref;
}

CRule *make_atom() {
  CRule *atom = new CRule(rule_type::ATOM);
  return atom;
}

CRule *make_epsilon() {
  CRule *epsilon = new CRule(rule_type::EPSILON);
  return epsilon;
}

CRule *make_marker(int id) {
  CRule *marker = new CRule(rule_type::MARKER);
  marker->_as_marker.id = id;
  return marker;
}

CRule *make_union(const std::vector<CRule *> &args,
                  const std::vector<std::vector<double> > &weights) {
  CRule *rule = new CRule(rule_type::UNION);

  rule->_as_union.args = new std::vector<CRule *>(args);
  rule->_as_union.weights = new std::vector<std::vector<double> >(weights);

  return rule;
}

CRule *make_product(const std::vector<CRule *> &args) {
  CRule *product_rule = new CRule(rule_type::PRODUCT);
  product_rule->_as_product.args = new std::vector<CRule *>(args);
  /* new (product_rule->_as_product.args) std::vector<CRule *>(args); */
  return product_rule;
}

CRule *make_seq(const CRule *arg, const std::vector<double> &weight,
                const std::vector<double> &arg_weight, int lower_size,
                int upper_size) {
  CRule *seq_rule = new CRule(rule_type::SEQ);

  seq_rule->_as_iterated_rule.weight = new std::vector<double>(weight);
  seq_rule->_as_iterated_rule.arg_weight = new std::vector<double>(arg_weight);
  /* Not sure we have to allocate this vector */
  seq_rule->_as_iterated_rule.partitions_weight =
      new std::vector<std::vector<double> >;

  seq_rule->_as_iterated_rule.arg = arg;
  seq_rule->_as_iterated_rule.upper_size = upper_size;
  seq_rule->_as_iterated_rule.lower_size = lower_size;

  return seq_rule;
}

CRule *make_set(const CRule *arg, const std::vector<double> &weight,
                const std::vector<double> &arg_weight, int lower_size,
                int upper_size) {
  CRule *set_rule = make_seq(arg, weight, arg_weight, lower_size, upper_size);
  set_rule->type = rule_type::SET;
  return set_rule;
}

CRule *make_mset(const CRule *arg, const std::vector<double> &weight,
                 const std::vector<double> &arg_weight,
                 const std::vector<std::vector<double> > &partitions_weight,
                 int lower_size, int upper_size) {
  CRule *mset_rule = make_seq(arg, weight, arg_weight, lower_size, upper_size);
  mset_rule->type = rule_type::MSET;
  mset_rule->_as_iterated_rule.partitions_weight =
      new std::vector<std::vector<double> >(partitions_weight);
  return mset_rule;
}

/* Probability distributions ****************************************/

int bnd_geometric(double param, int lower_bound, int upper_bound) {
  const double r = rand_double();
  int bounding_term = 0;
  lower_bound = lower_bound < 0 ? 0 : lower_bound;

  if (upper_bound > 0) {
    const int k = upper_bound - lower_bound;
    bounding_term = (1 - r) * std::pow(1 - param, (k + 1));
  }

  double geom = std::floor(std::log(r + bounding_term) / std::log(1 - param));
  return static_cast<int>(geom) + lower_bound;
}

int bnd_poisson(double total_weight, double param, int lower_bound,
                int upper_bound) {
  const double r = rand_double() * total_weight;
  double s = 0;
  int i = lower_bound > 0 ? lower_bound : 0;

  while (s < r) {
    s = s + std::pow(param, i) / std::tgamma(i + 1);
    i++;
  }

  if (upper_bound > 0 && i > upper_bound + 1) // XXX. Why?
    return bnd_poisson(total_weight, param, lower_bound, upper_bound);
  else
    return (i - 1);
}

/* Next parition in lexicographic order (encoded as a multiset)
 * Runs in constant time, thus allowing to enumerate all partitions in constant
 * amortised time.
 * REF: Frank Ruskey, Combinatorial Generation (not published yet),
 * page 97 of working version 1j-CSC 425/520 available at:
 * https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
 *
 * Implementation note: For convenience, Rusky sets a pair at index -1 of the
 array (in
 * C's sense, not in Python's sense). We offset all the indices by one to avoid
 dealing
 * with negatives indices. The initial partition is thus [[0, 0], [n+1,0], [1,
 n]] and
 * the variable l in the Ruskey's book must be thought of as the index of the
 last
 * component of the partition.

 * This function expects a valid partition (undefined behaviour otherwise) and
 returns
 * True if and only if the argument is the last partition (in lex order). */
bool next_partition(std::vector<std::pair<int, int> > &part) {
  int sum = part.back().first * part.back().second;

  if (part.back().second == 1) {
    part.pop_back();
    sum += part.back().first * part.back().second;
  }

  if ((part.end() - 2)->first == part.back().first + 1) {
    part.pop_back();
    part.back().second++;
  } else {
    part.back().first++;
    part.back().second = 1;
  }

  if (sum > part.back().first) {
    part.push_back(std::make_pair(1, sum - part.back().first));
  }

  return part.size() == 2;
}

std::vector<std::pair<int, int> > initial_partition(int k) {
  std::vector<std::pair<int, int> > v;

  v.push_back(std::make_pair(0, 0));
  v.push_back(std::make_pair(k + 1, 0));
  v.push_back(std::make_pair(1, k));

  return v;
}

int bnd_mset_dist(const std::vector<double> &total_weight,
                  const std::vector<double> &arg_weight, int multiplicity) {
  const double r = rand_double() * total_weight[multiplicity];
  const int max_multiplicity = total_weight.size();

  double acc = 1.0;
  int i = 1; // Next value to try

  while (i * multiplicity < max_multiplicity) {
    if (r < acc)
      return i - 1;
    acc *= exp(arg_weight[i * multiplicity] / i);
    i++;
  }

  // Should not reach this point
  throw std::logic_error("It should be impossible to reach this point.");
}

void show_rule(const CRule *rule) {
  std::cout << std::flush;
  switch (rule->type) {
  case EPSILON:
    std::cout << "eps";
    break;
  case ATOM: {
    std::cout << "z";
  } break;
  case MARKER: {
    int id = rule->_as_marker.id;
    std::cout << "u" << id;
  } break;
  case REF: {
    std::cout << "REF[" << rule->_as_ref.rule << "]";
  } break;
  case UNION: {
    std::cout << "(";
    auto arg = rule->_as_union.args->begin();
    auto ws = rule->_as_union.weights->begin();
    std::cout << "[" << (*ws)[1] << " -> ";
    show_rule(*arg);
    std::cout << "]";
    arg++;
    ws++;
    while (arg != rule->_as_union.args->end()) {
      std::cout << " + ";
      std::cout << "[" << (*ws)[1] << " -> ";
      show_rule(*arg);
      std::cout << "]";
      arg++;
    }
    std::cout << ")";
  } break;
  case PRODUCT: {
    std::cout << "(";
    auto arg = rule->_as_product.args->begin();
    show_rule(*arg);
    arg++;
    while (arg != rule->_as_product.args->end()) {
      std::cout << " * ";
      show_rule(*arg);
      arg++;
    }
    std::cout << ")";
  } break;
  case SET: {
    auto r = rule->_as_iterated_rule;
    std::cout << "SET(";
    show_rule(r.arg);
    std::cout << ", lower_size=" << r.lower_size;
    std::cout << ", upper_size=" << r.upper_size;
    std::cout << ")";
  } break;
  case SEQ: {
    auto r = rule->_as_iterated_rule;
    std::cout << "SEQ(";
    show_rule(r.arg);
    std::cout << ", lower_size=" << r.lower_size;
    std::cout << ", upper_size=" << r.upper_size;
    std::cout << ")";
  } break;
  case MSET: {
    auto r = rule->_as_iterated_rule;
    std::cout << "MSET(";
    show_rule(r.arg);
    std::cout << ", lower_size=" << r.lower_size;
    std::cout << ", upper_size=" << r.upper_size;
    std::cout << ")";
  } break;
  default:
    throw std::invalid_argument("There is a problem with your grammar."
                                "Please report it to the developpers.");
  }
}

CRule *CRule::make_set_mult(int mult) {
  CRule *rule = new CRule(rule_type::SET_MULTIPLICITY);
  rule->_as_set_mult.multiplicity = mult;
  return rule;
}

std::vector<int> c_simulate(const CRule *first_rule,
                            const std::vector<int> &max_sizes) {
  std::vector<int> sizes(max_sizes.size());
  std::stack<const CRule *> todo;

  todo.push(first_rule);

  double r;
  int multiplicity = 1;

  while (!todo.empty()) {
    const CRule *rule = todo.top();
    todo.pop();

    switch (rule->type) {
    case EPSILON:
      break;
    case ATOM: {
      sizes[0] += multiplicity;
      if (max_sizes[0] > 0 && sizes[0] > max_sizes[0])
        return sizes;
    } break;
    case MARKER: {
      // NB: Marker ids start at zero but sizes[0] stores the number of atoms
      // of the structure under simulation.
      const int index = rule->_as_marker.id + 1;
      sizes[index] += multiplicity;
      if (max_sizes[index] > 0 && sizes[index] > max_sizes[index])
        return sizes;
    } break;
    case REF: {
      todo.push(rule->_as_ref.rule);
    } break;
    case UNION: {
      r = rand_double();
      auto arg = rule->_as_union.args->begin();
      auto ws = rule->_as_union.weights->begin();
      while (arg != rule->_as_union.args->end()) {
        r = r - (*ws)[multiplicity];
        if (r <= 0) {
          todo.push(*arg);
          break;
        }
        arg++;
        ws++;
      }
    } break;
    case PRODUCT: {
      for (auto &arg : *rule->_as_product.args)
        todo.push(arg);
    } break;
    case SEQ: {
      const auto seq = rule->_as_iterated_rule;
      const int k = bnd_geometric(1 - (*seq.arg_weight)[multiplicity],
                                  seq.lower_size, seq.upper_size);
      for (int i = 0; i < k; i++)
        todo.push(seq.arg);
    } break;
    case SET: {
      const auto &set = rule->_as_iterated_rule;
      const int k = bnd_poisson((*set.weight)[multiplicity],
                                (*set.arg_weight)[multiplicity], set.lower_size,
                                set.upper_size);
      for (int i = 0; i < k; i++)
        todo.push(set.arg);
    } break;
    case MSET: {
      const auto mset = rule->_as_iterated_rule;

      // Save the current multiplicity.
      todo.push(CRule::make_set_mult(multiplicity));

      // Upper-bounded MSets
      if (mset.upper_size >= 0) {
        if (mset.lower_size < mset.upper_size) {
          throw std::invalid_argument("MSet with bounds other than `eq=...`");
        }

        // Draw a partition under the distribution induced by their weights:
        auto partition = initial_partition(mset.lower_size);
        auto pw = mset.partitions_weight->begin();
        double r = rand_double() * (*mset.weight)[multiplicity];
        r -= (*pw)[multiplicity];
        while (r > 0) {
          pw++;
          next_partition(partition);
          r -= (*pw)[multiplicity];
        };

        // Set up the recursive calls for that partition:
        for (auto &p : partition) {
          // Draw p.second independent elements...
          for (int j = 0; j < p.second; j++) {
            todo.push(mset.arg);
          }
          // ... with multiplicity p.first (times the current multiplicity).
          todo.push(CRule::make_set_mult(p.first * multiplicity));
        }

        // Lower-bounded MSets
      } else if (mset.lower_size > 0) {
        throw std::invalid_argument("Lower-bounded MSet with no upper bound");

        // Unbounded MSets
      } else {
        const int k =
            bnd_mset_dist(*mset.weight, *mset.arg_weight, multiplicity);

        double param;
        int nb;

        for (int j = 1; j < k; j++) {
          // nb = Poisson (A(z^{j m}) / j)
          param = (*mset.arg_weight)[j * multiplicity] / j;
          nb = bnd_poisson(exp(param), param, 0, -1);
          // Generate nb arguments with multiplicity `j * multiplicity`
          for (; nb; nb--)
            todo.push(mset.arg);
          todo.push(CRule::make_set_mult(j * multiplicity));
        }

        if (k > 0) {
          // nb = Poisson_{> 0} (A(z^{k m}) / k)
          param = (*mset.arg_weight)[k * multiplicity] / k;
          nb = bnd_poisson(exp(param) - 1.0, param, 1, -1);
          // Generate nb arguments with multiplicity `k * multiplicity`
          for (; nb; nb--)
            todo.push(mset.arg);
          todo.push(CRule::make_set_mult(k * multiplicity));
        }
      }

    } break;
    case SET_MULTIPLICITY: {
      multiplicity = rule->_as_set_mult.multiplicity;
    } break;
    default:
      throw std::invalid_argument("There is a problem with your grammar."
                                  "Please report it to the developpers.");
    }
  }

  return sizes;
}

// bool in_window(std::vector<int>& sizes,
//                 std::vector<int>& min_sizes,
//                 std::vector<int>& max_sizes){
//   for(auto i = 0; i < sizes.size(); i++)
//     if(sizes[i] < min_sizes[i] || sizes[i] > max_sizes[i])
//       return false;
//   return true;
// }

// std::vector<int>&& rand_perm(int n){
//   int i, j;
//   std::vector<int> p;

//   for(int i = 1; i <= n; i++)
//     p->push_back(i);

//   for(int i = n-1; i>0; i--){
//     j = rand_i64(i);
//     std::swap(*p[i], *p[j]);
//   }

//   return std::move(p);
// }

// std::vector<int> c_search_seed(Rule* first_rule,
//                               std::vector<int>& min_sizes,
//                               std::vector<int>& max_sizes,
//                               bool labelling){
//   xhoshiro::randstate backup_state;
//   get_state(backup_state);
//   std::vector<int> sizes = simulate(first_rule, max_sizes);

//   while(!in_window(sizes, min_sizes, max_sizes)){
//     // save the random generator's state
//     get_state(backup_state);
//     sizes = simulate(first_rule, max_sizes);
//   }
//   // Generate the labels BEFORE reseting the RNG
//   std::vector<int> labels;
//   if(labelling)
//     labels = rand_perm(sizes[0]);

//   // Reset the random generator to the state it was just before the
//   simulation xoshiro.set_state(backup_state); return labels;
// }

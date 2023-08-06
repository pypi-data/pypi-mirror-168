#ifndef __SIMULATOR_HPP_
#define __SIMULATOR_HPP_

/*
Copyright 2019-2022 Matthieu Dien and Martin Pépin
Distributed under the license GNU GPL v3 or later
See LICENSE.txt for more informations
*/

#include <vector>

typedef enum {
  // Symbols
  REF,
  ATOM,
  MARKER,
  EPSILON,
  // Grammar combinators
  UNION,
  PRODUCT,
  SEQ,
  SET,
  MSET,
  // A special symbol for the simulation stack machine.
  // Never put this in a grammar.
  SET_MULTIPLICITY
} rule_type;

class CRule {

private:
  union {
    struct {
      int id;
      CRule *rule;
    } _as_ref;

    struct {
      int id;
    } _as_marker;

    // Product
    struct {
      std::vector<CRule *> *args;
    } _as_product;

    // Union
    struct {
      std::vector<CRule *> *args;
      std::vector<std::vector<double> > *weights;
    } _as_union;

    // Iterated rules
    struct {
      const CRule *arg;
      int lower_size;
      int upper_size;
      // For Seqs, Sets, and unbounded MSets, these two fields are sufficient
      std::vector<double> *weight;
      std::vector<double> *arg_weight;
      // For exact-size MSet sampling, this extra field stores the weights of
      // each (integer) partition of the MSet size. Each element of the vector
      // stores the weights (for z^j for j > 0) of a partition. The partitions
      // are considered in lexicographic order.
      std::vector<std::vector<double> > *partitions_weight;
    } _as_iterated_rule;

    // A special symbol for the simulation stack machine.
    // Never put this in a grammar.
    struct {
      int multiplicity;
    } _as_set_mult;
  };

  CRule();
  CRule(rule_type t) : type(t){};

  rule_type type;

  static CRule *make_set_mult(int mult);

public:
  rule_type get_type() const;

  int get_ref_id() const;
  void set_ref_rule(CRule *rule);
  const CRule *get_ref_rule() const;

  int get_marker_id() const;

  const std::vector<CRule *> &get_product_args() const;

  const std::vector<CRule *> &get_union_args() const;
  const std::vector<std::vector<double> > &get_union_weights() const;

  const CRule *get_iter_arg() const;
  const std::vector<double> &get_iter_weight() const;
  const std::vector<double> &get_iter_arg_weight() const;
  const std::vector<std::vector<double> > &get_mset_partitions_weight() const;
  int get_iter_lower_size() const;
  int get_iter_upper_size() const;

  friend CRule *make_ref(int id);
  friend CRule *make_atom();
  friend CRule *make_epsilon();
  friend CRule *make_marker(int id);
  friend CRule *make_union(const std::vector<CRule *> &args,
                           const std::vector<std::vector<double> > &weights);
  friend CRule *make_product(const std::vector<CRule *> &args);
  friend CRule *make_seq(const CRule *arg, const std::vector<double> &weight,
                         const std::vector<double> &arg_weight, int lower_size,
                         int upper_size);
  friend CRule *make_set(const CRule *arg, const std::vector<double> &weight,
                         const std::vector<double> &arg_weight, int lower_size,
                         int upper_size);
  friend CRule *
  make_mset(const CRule *arg, const std::vector<double> &weight,
            const std::vector<double> &arg_weight,
            const std::vector<std::vector<double> > &partitions_weight,
            int lower_size, int upper_size);

  friend std::vector<int> c_simulate(const CRule *first_rule,
                                     const std::vector<int> &max_sizes);

  friend void show_rule(const CRule *rule);
};

int bnd_geometric(double param, int lower_bound, int upper_bound);
int bnd_poisson(double total_weight, double param, int lower_bound,
                int upper_bound);
int bnd_mset_dist(std::vector<double> const &total_weight,
                  std::vector<double> const &arg_weight, int multiplicity);
std::vector<std::pair<int, int> > initial_partition(int k);
bool next_partition(std::vector<std::pair<int, int> > &part);

#endif

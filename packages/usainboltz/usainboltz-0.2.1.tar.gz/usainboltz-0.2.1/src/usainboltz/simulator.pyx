# distutils: language = c++
# cython: language_level = 3

# Copyright 2019-2022 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

from libc.math cimport exp, pow, tgamma
from libcpp.utility cimport pair
from libcpp.vector cimport vector

from usainboltz.cpp_simulator cimport (
    CRule,
    bnd_geometric,
    bnd_mset_dist,
    bnd_poisson,
    c_simulate,
    get_state,
    initial_partition,
    make_atom,
    make_epsilon,
    make_marker,
    make_mset,
    make_product,
    make_ref,
    make_seq,
    make_set,
    make_union,
    next_partition,
    rand_double,
    rand_i64,
    seed,
    set_state,
)

from usainboltz.grammar import (
    Atom,
    Epsilon,
    Marker,
    MSet,
    Product,
    RuleName,
    Seq,
    Set,
    Symbol,
    Union,
)

# --- Wrapper on top of basic distributions implemented in C++ ------


cpdef int bounded_geometric(double d, int n, int m):
    return bnd_geometric(d,n,m)

cpdef int bounded_poisson(double a, double b, int c, int d):
    return bnd_poisson(a,b,c,d)

cpdef int bounded_mset_distribution(list weights, list arg_weights, int multiplicity):
    return bnd_mset_dist(weights, arg_weights, multiplicity)


# --- Wrapper on top of the C++ simulator ---------------------------


cdef double partition_weight(vector[pair[int, int]] part,
                             vector[double] arg_weight,
                             int j) except *:
    cdef double res = 1.0
    cdef int v, m, d = arg_weight.size()

    for v, m in part:
        if v * j < d:
            res *= pow(arg_weight[v * j], m)
            res /= tgamma(m + 1)
            res /= pow(v, m)

    return res


cdef class Simulator:
    def __init__(self, grammar, weights, mapping):
        self.mapping = mapping
        self.grammar_to_c_struct(grammar, weights)

    cdef void grammar_to_c_struct(self, object grammar, dict weights) except *:
        """Conversion of a Python grammar into a C++ grammar"""

        cdef pair[int, CRule*] binding

        # Allocate C rules for Epsilon() and Atom()
        self.c_epsilon = make_epsilon()
        self.c_atom = make_atom()

        # Allocate one C rule per Marker()
        for marker in grammar.markers():
            binding.first = self.mapping.marker_to_id[marker]
            binding.second = make_marker(binding.first)
            self.c_markers.insert(binding)

        # Allocate one C rule per RuleName()
        for rule_name in grammar.rules:
            binding.first = self.mapping.rule_name_to_id[rule_name]
            binding.second = make_ref(binding.first)
            self.c_rules.insert(binding)

        # Generate C rules for the right-hand-side of each grammar rule and bind them to
        # their rule name.
        cdef CRule *rule
        cdef wrule body
        for rule_name, rule_body in grammar.rules.items():
            rule = self.c_rules[self.mapping.rule_name_to_id[rule_name]]
            body = self.rule_to_c_struct(rule_body, weights)
            rule.set_ref_rule(body.rule)

    cpdef list run(self, object rulename, list max_sizes):
        cdef vector[int] ms = max_sizes
        cdef CRule* start = self.c_rules[self.mapping.rule_name_to_id[rulename]]
        return c_simulate(start, ms)

    cdef wrule rule_to_c_struct(self, object rule, dict weights) except *:
        cdef wrule res
        cdef int ls, us

        if isinstance(rule, Symbol):
            if isinstance(rule, Epsilon):
                res.rule = self.c_epsilon
            elif isinstance(rule, Atom):
                res.rule = self.c_atom
            elif isinstance(rule, Marker):
                res.rule = self.c_markers[self.mapping.marker_to_id[rule]]
            elif isinstance(rule, RuleName):
                res.rule = self.c_rules[self.mapping.rule_name_to_id[rule]]
            else:
                assert False
            res.weights = weights[rule]
            return res
        elif isinstance(rule, Union):
            return self.union_to_c_struct(rule.args, weights)
        elif isinstance(rule, Product):
            return self.product_to_c_struct(rule.args, weights)
        elif isinstance(rule, Seq):
            ls = 0 if rule.lower_size is None else rule.lower_size
            us = -1 if rule.upper_size is None else rule.upper_size
            return self.seq_to_c_struct(rule.arg, ls, us, weights)
        elif isinstance(rule, Set):
            ls = 0 if rule.lower_size is None else rule.lower_size
            us = -1 if rule.upper_size is None else rule.upper_size
            return self.set_to_c_struct(rule.arg, ls, us, weights)
        elif isinstance(rule, MSet):
            ls = 0 if rule.lower_size is None else rule.lower_size
            us = -1 if rule.upper_size is None else rule.upper_size
            return self.mset_to_c_struct(rule.arg, ls, us, weights)
        else:
            raise NotImplementedError(f"Operator {type(rule)} not yet supported.")

    cdef wrule union_to_c_struct(self, args, dict weights) except *:
        cdef wrule res, tmp
        cdef vector[vector[double]] probabilities
        cdef vector[CRule_ptr] c_args
        cdef int i, j, d = len(weights[Atom()]), nargs = len(args)

        c_args.clear()
        res.weights = [0.0] * d
        probabilities = [[0.0] * d for _ in range(nargs)]

        for i, arg in enumerate(args):
            tmp = self.rule_to_c_struct(arg, weights)
            c_args.push_back(tmp.rule)
            for j in range(1, d):
                probabilities[i][j] = tmp.weights[j]
                res.weights[j] += tmp.weights[j]
        for i in range(nargs):
            for j in range(1, d):
                if res.weights[j] > 0:
                    probabilities[i][j] /= res.weights[j]
        assert(c_args.size() > 1)
        res.rule = make_union(c_args, probabilities)
        return res

    cdef wrule product_to_c_struct(self, args, dict weights) except *:
        cdef wrule res, tmp
        cdef vector[CRule_ptr] c_args
        cdef int j, d = len(weights[Atom()])

        c_args.clear()
        res.weights = [1.0] * d

        for arg in args:
            tmp = self.rule_to_c_struct(arg, weights)
            c_args.push_back(tmp.rule)
            for j in range(1, d):
                res.weights[j] *= tmp.weights[j]
        res.rule = make_product(c_args)
        return res

    cdef wrule seq_to_c_struct(self, arg, int lower_size, int upper_size, dict weights) except *:
        cdef wrule res, c_arg
        cdef int j, d = len(weights[Atom()])
        cdef double ps_inv

        res.weights = [0.0] * d
        res.weights[0] = 1.0
        c_arg = self.rule_to_c_struct(arg, weights)

        for j in range(1, d):
            ps_inv = 1 / (1 - c_arg.weights[j])
            res.weights[j] = ps_inv
            res.weights[j] *= c_arg.weights[j] ** lower_size
            if upper_size > 0:
                res.weights[j] -= ps_inv * c_arg.weights[j] ** (upper_size + 1)
        res.rule = make_seq(
            c_arg.rule, res.weights, c_arg.weights, lower_size, upper_size
        )
        return res

    cdef wrule set_to_c_struct(self, arg, int lower_size, int upper_size, dict weights) except *:
        cdef wrule res, c_arg
        cdef int i, j, d = len(weights[Atom()])

        res.weights = [0.0] * d
        res.weights[0] = 1.0
        c_arg = self.rule_to_c_struct(arg, weights)

        for j in range(1, d):
            if upper_size > 0:
                for i in range(upper_size + 1):
                    res.weights[j] += c_arg.weights[j] ** i / tgamma(i + 1)
            else:
                res.weights[j] = exp(c_arg.weights[j])
                for i in range(lower_size):
                    res.weights[j] -= c_arg.weights[j] ** i / tgamma(i + 1)
        res.rule = make_set(
            c_arg.rule, res.weights, c_arg.weights, lower_size, upper_size
        )
        return res

    cdef wrule mset_to_c_struct(self, arg, int lower_size, int upper_size, dict weights) except *:
        cdef wrule res, c_arg
        cdef int i, j, d = len(weights[Atom()])
        cdef double acc
        cdef vector[vector[double]] partitions_weight
        cdef vector[pair[int, int]] partition

        res.weights = [0.0] * d
        res.weights[0] = 1.0
        c_arg = self.rule_to_c_struct(arg, weights)

        # M(z) = MSet_{lower_size <= . <= upper_size}(A)(z)
        if upper_size >= 0:
            if lower_size < upper_size:
                raise NotImplementedError("MSet with bounds other than `eq=...`")
            upper_size = min(d - 1, upper_size)
            lower_size = min(d - 1, lower_size)

            partition = initial_partition(lower_size)
            done = False
            while not done:
                part_weight = [0.0]
                for j in range(1, d):
                    # The weight of the current partition at z^j
                    acc = partition_weight(partition, c_arg.weights, j)
                    part_weight.append(acc)
                    res.weights[j] += acc
                partitions_weight.push_back(part_weight)
                done = next_partition(partition)
        elif lower_size > 0:
            raise NotImplementedError("Lower-bounded MSet with no upper bound")
        # M(z) = MSet(A)(z)
        else:
            for j in range(1, d):
                i = 1
                acc = 1.0
                while i * j < d:
                    acc *= exp(c_arg.weights[i * j] / i)
                    i += 1
                res.weights[j] = acc

        res.rule = make_mset(
            c_arg.rule,
            res.weights,
            c_arg.weights,
            partitions_weight,
            lower_size,
            upper_size
        )
        return res


# --- Wrapper on top of PRNG functions ------------------------------


cpdef void rng_seed(uint64_t s):
    seed(s)


cpdef double rng_double():
    return rand_double()


cpdef int64_t rng_i64(int64_t bound):
    return rand_i64(bound)


cdef void rng_get_state(uint64_t dest[4]):
    get_state(dest)


cdef void rng_set_state(const uint64_t s[4]):
    set_state(s)

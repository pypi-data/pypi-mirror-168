# cython: language_level = 3

# Copyright 2019-2022 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

from libc.stdint cimport int64_t, uint64_t
from libcpp.pair cimport pair
from libcpp.vector cimport vector


cdef extern from "cpp_simulator.cpp":
    pass

cdef extern from "cpp_xoshiro.cpp":
    pass

cdef extern from "cpp_simulator.hpp":
    ctypedef enum rule_type:
        REF,
        ATOM,
        MARKER,
        EPSILON,
        UNION,
        PRODUCT,
        SEQ,
        SET,
        MSET,

    cdef cppclass CRule:
        rule_type get_type()

        int get_ref_id()
        void set_ref_rule(CRule*)
        CRule *get_ref_rule()

        int get_marker_id()

        const vector[CRule*] &get_product_args()

        const vector[CRule*] &get_union_args()
        const vector[vector[double]] &get_union_weights()

        const CRule* get_iter_arg()
        const vector[double] &get_iter_weight()
        const vector[double] &get_iter_arg_weight()
        int get_iter_lower_size()
        int get_iter_upper_size()
        const vector[vector[double]] &get_mset_partitions_weight()

    CRule* make_ref(int)
    CRule* make_atom()
    CRule* make_epsilon()
    CRule* make_marker(int)
    CRule* make_union(vector[CRule*] &args, vector[vector[double]] & weights)
    CRule* make_product(vector[CRule*]& args)
    CRule* make_seq(CRule*, vector[double], vector[double], int, int)
    CRule* make_set(CRule*, vector[double], vector[double], int, int);
    CRule* make_mset(CRule*, vector[double], vector[double], vector[vector[double]],
                     int, int);

    int bnd_geometric(double, int, int)
    int bnd_poisson(double, double, int, int)
    int bnd_mset_dist(vector[double], vector[double], int) except +

    vector[pair[int, int]] initial_partition(int)
    bint next_partition(vector[pair[int, int]]&) except +

    vector[int] c_simulate(CRule*, vector[int]& max_sizes) except +

cdef extern from "cpp_xoshiro.hpp":
    double rand_double()
    int64_t rand_i64(const int64_t bound)

    void seed(const uint64_t seed)
    void get_state(uint64_t dest[4])
    void set_state(const uint64_t s[4])

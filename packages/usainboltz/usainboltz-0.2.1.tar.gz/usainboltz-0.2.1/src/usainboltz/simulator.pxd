# distutils: language = c++
# cython: language_level = 3

# Copyright 2019-2022 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

from libc.stdint cimport int64_t, uint64_t
from libcpp.map cimport map as cpp_map
from libcpp.pair cimport pair
from libcpp.vector cimport vector

from usainboltz.cpp_simulator cimport CRule


cpdef int bounded_geometric(double, int, int);
cpdef int bounded_poisson(double, double, int, int);
cpdef int bounded_mset_distribution(list, list, int);


# CRule* is valid syntax wherever the cython parser expects a type, but not inside
# brackets e.g. when applying C++ templates.
# To work around this issue we define an alise for CRule*
ctypedef CRule* CRule_ptr

ctypedef struct wrule:
    CRule* rule
    vector[double] weights

cdef class Simulator:
    cdef CRule *c_epsilon
    cdef CRule *c_atom
    cdef cpp_map[int, CRule*] c_markers
    cdef cpp_map[int, CRule*] c_rules
    cdef object mapping

    cdef void grammar_to_c_struct(self, object, dict) except *
    cpdef list run(self, object, list)
    cdef wrule rule_to_c_struct(self, object, dict) except *
    cdef wrule union_to_c_struct(self, object, dict) except *
    cdef wrule product_to_c_struct(self, object, dict) except *
    cdef wrule seq_to_c_struct(self, object, int, int, dict) except *
    cdef wrule set_to_c_struct(self, object, int, int, dict) except *
    cdef wrule mset_to_c_struct(self, object, int, int, dict) except *

# Xoshiro stuff
cpdef void rng_seed(uint64_t)
cpdef double rng_double()
cpdef int64_t rng_i64(int64_t)
cdef void rng_get_state(uint64_t dest[4])
cdef void rng_set_state(const uint64_t s[4])

# coding: utf-8

# distutils: sources = cpp_xoshiro.cpp
# cython: language_level = 3

# Copyright 2019-2022 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

from libc.stdint cimport int64_t, uint64_t


cdef extern from "cpp_xoshiro.hpp":
    double rand_double()
    int64_t rand_i64(const int64_t bound)

    void seed(const uint64_t seed)
    void get_state(uint64_t dest[4])
    void set_state(const uint64_t s[4])

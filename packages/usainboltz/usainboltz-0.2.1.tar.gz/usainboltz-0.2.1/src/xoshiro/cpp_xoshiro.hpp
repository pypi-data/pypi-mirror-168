/*
Copyright 2019-2022 Matthieu Dien and Martin Pépin
Distributed under the license GNU GPL v3 or later
See LICENSE.txt for more informations
*/

#ifndef XOSHIRO_H
#define XOSHIRO_H 1

/*
This is xoshiro256++ 1.0, a rock-solid general purpose generator.

The seed function fills the random state using a splitmix64 algorithm as
suggested by the authors of xoshiro256++.

More details about both algorithms at <http://prng.di.unimi.it/>.
*/

#include <cstdint>

typedef uint64_t randstate[4];

double rand_double();
long int rand_i64(const int64_t);

void seed(const uint64_t);
void get_state(uint64_t[4]);
void set_state(const uint64_t[4]);

#endif

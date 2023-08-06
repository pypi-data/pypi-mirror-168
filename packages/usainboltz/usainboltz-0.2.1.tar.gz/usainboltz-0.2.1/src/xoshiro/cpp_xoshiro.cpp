/*
Copyright 2019-2022 Matthieu Dien and Martin Pépin
Distributed under the license GNU GPL v3 or later
See LICENSE.txt for more informations
*/

/*
This is xoshiro256++ 1.0, a rock-solid general purpose generator.

The seed function fills the random state using a splitmix64 algorithm as
suggested by the authors of xoshiro256++.

More details about both algorithms at <http://prng.di.unimi.it/>.
*/

#include "cpp_xoshiro.hpp"
#include <cstdint>

/* xoshiro256++ code ************************************************/

static inline uint64_t rotl(const uint64_t x, int k) {
  return (x << k) | (x >> (64 - k));
}

static randstate state = {0x31a0da5e61a2e459l, 0xe68b3048ea5f11a5l,
                          0xbd0fbca6c09e762al, 0x1ea62c6af476c5e9l};

uint64_t next(void) {
  const uint64_t result = rotl(state[0] + state[3], 23) + state[0];
  const uint64_t t = state[1] << 17;

  state[2] ^= state[0];
  state[3] ^= state[1];
  state[1] ^= state[2];
  state[0] ^= state[3];
  state[2] ^= t;
  state[3] = rotl(state[3], 45);

  return result;
}

/* Wrapper for generating bounded integers and doubles **************/

// Uniform doubles in the interval [0; 1[
double rand_double() {
  uint64_t n = next();
  /* I would like to write:
   * return (n >> 11) * 0x1.0p-53;
   * but the 0x${MANTISSA}p${EXPONENT} notation is not available in prior to
   * c++17.
   * This should be the same number. */
  return (n >> 11) * 1.11022302462515654e-16;
}

// Uniform integers in the interval [0; bound[.
long int rand_i64(const int64_t bound) {
  const int64_t r = next() >> 4;
  const int64_t v = r % bound;
  if (r - v > ((1l << 61) - 1) - bound + 1) {
    return rand_i64(bound);
  } else {
    return v;
  }
}

/* State seeding using splitmix64 ***********************************/

// Source: http://prng.di.unimi.it/splitmix64.c
uint64_t splitmix64(uint64_t *x) {
  uint64_t z = (*x += 0x9e3779b97f4a7c15);
  z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9;
  z = (z ^ (z >> 27)) * 0x94d049bb133111eb;
  z = z ^ (z >> 31);
  return z;
}

void seed(const uint64_t seed) {
  uint64_t x = seed;

  for (int i = 0; i < 4; i++) {
    state[i] = splitmix64(&x);
  }
}

/* Getter and setter for the PRNG state *****************************/

void get_state(randstate dest) {
  for (int i = 0; i < 4; i++) {
    dest[i] = state[i];
  }
}

void set_state(const randstate s) {
  for (int i = 0; i < 4; i++) {
    state[i] = s[i];
  }
}

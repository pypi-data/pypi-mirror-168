# Copyright 2019-2022 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

"""A Boltzmann sampler for Pólya n-ary trees.

>>> from usainboltz import *
>>> from usainboltz.generator import rng_seed
>>> rng_seed(0xDEADBEEFB017)  # For reproducibility

Pólya trees are unlabelled unordered rooted trees. They are specified using the
:py:class:`~usainboltz.grammar.MSet` operator:

>>> z = Atom()
>>> T = RuleName("T")
>>> grammar = Grammar({T: z * MSet(T)})
>>> grammar
{
  T : Product(z, MSet(T))
}

The singularity of theses trees is near z = 0.33832185689920769 (cf. [FS2009] section
VII.5 page 475) and the value of the generating function at this point is 1.
Let us check that the oracle finds these values:

>>> oracle = build_oracle(grammar)
>>> values = oracle.tuning(z, singular=True)
>>> # NB: values[z][j] stores the value of z^j
>>> print(f"{values[z][1]:.6f}")
0.338322
>>> print(f"{values[T][1]:.6f}")
1.000000

Now, let us generate a Pólya tree:
>>> generator = Generator(grammar)
>>> res = generator.sample((10, 15))
>>> print(res.obj)
('z', [('z', []),
       ('z', [('z', []),
              ('z', []),
              ('z', [('z', []),
                     ('z', [('z', []),
                            ('z', []),
                            ('z', []),
                            ('z', []),
                            ('z', [])])])])])

Finally, let us check that the number of atoms in the structure corresponds to the
size reported by the generator.
>>> def compute_size(tree):
...     _, mset = tree
...     return 1 + sum((compute_size(tree) for tree in mset))
>>> res.sizes[z] == compute_size(res.obj), res.sizes[z]
(True, 13)
"""

from usainboltz import Atom, Generator, Grammar, MSet, RuleName

if __name__ == "__main__":
    # Construct the grammar
    z = Atom()
    T = RuleName("T")
    grammar = Grammar({T: z * MSet(T)})

    # Instatiate the generator
    gen = Generator(grammar)
    for _ in range(10):
        print(gen.sample((20, 30)))

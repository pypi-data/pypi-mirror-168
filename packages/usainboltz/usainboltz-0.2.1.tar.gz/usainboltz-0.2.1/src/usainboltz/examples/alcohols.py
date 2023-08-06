# Copyright 2019-2022 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

r"""A Boltzmann sampler for alcohols

>>> from usainboltz import *
>>> from usainboltz.generator import rng_seed
>>> rng_seed(0xDEADBEEFB0175)  # For reproducibility

According to [FS2009] page 477, alcohols can been seen as rooted non-plane trees of
degree 3. The carbonic skeleton gives the tree structure and the carbon atom to which
the (unique) -OH group is attached is the root of the tree.
We thus use the :py:class:`~usainboltz.grammar.MSet` together with the :code:`eq=3`
constraint to specify these trees.

>>> carbon = Atom()
>>> A = RuleName("A")  # A for alcohol
>>> hydrogen = Marker("H")
>>> grammar = Grammar({A: hydrogen + carbon * MSet(A, eq=3)})
>>> grammar
{
  A : Union(H, Product(z, MSet(A, eq = 3)))
}

According to [FS2009], the singularity of the generating function of alcohols is near
0.35518174. Let us verify that the oracle finds a similar value.

>>> oracle = build_oracle(grammar)
>>> values = oracle.tuning(carbon, singular=True)
>>> print(f"{values[carbon][1]:.8f}")
0.35518174

The tree representation does not help a lot to visualise the molecule so let us define a
custom data structure for representing alcohols

>>> class Alcohol:
...     def __init__(self, *args):
...         main_builder = union_builder(self._init_hydrogen, self._init_carbon)
...         main_builder(*args)
...
...     def _init_hydrogen(self, epsilon):
...         self.element = "H"
...
...     def _init_carbon(self, args):
...         c, children = args
...         self.element = "C"
...         self.children = children
...
...     def to_dot(self):
...         # Print in graphviz format
...         print('graph {\n  node [shape="none", width=0.4, height=0.4]')
...         root_id = self._to_dot(0)
...         print('  root_node [label="OH"]')
...         print(f"  root_node -- node{root_id}")
...         print("}")
...
...     def _to_dot(self, counter):
...         # counter is the id of the last printed object
...         if self.element == "H":
...             counter += 1
...             print(f'  node{counter} [label="H"]')
...             return counter
...         else:
...             children_names = []
...             for c in self.children:
...                 counter = c._to_dot(counter)
...                 children_names.append(f"node{counter}")
...             counter += 1
...             print(f'  node{counter} [label="C"]')
...             print(f'  node{counter} -- {{{" ".join(children_names)}}}')
...             return counter

We defined the __init__ method of our class so that it can be passed directly to the
generator as a builder. Let us to so and run the random sampler:

>>> generator = Generator(grammar)
>>> generator.set_builder(A, Alcohol)  # pass the class constructor directly
>>> res = generator.sample((10, 15))

We generated an alcohol with the following elements:

>>> SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
>>> nb_carbons = str(res.sizes[carbon]).translate(SUB)
>>> nb_hydrogens = str(res.sizes[hydrogen] + 1).translate(SUB)
>>> print(f"C{nb_carbons}OH{nb_hydrogens}")
C₁₅OH₃₂

Using the printer we defined above, we can print a DOT reprensetation of the generated
alcohol:

>>> res.obj.to_dot()  # doctest: +ELLIPSIS
graph {
  node [shape="none", width=0.4, height=0.4]
  node1 [label="H"]
  node2 [label="H"]
  node3 [label="H"]
  node4 [label="C"]
  node4 -- {node1 node2 node3}
  node5 [label="H"]
...

Using the neato rendered of the graphviz library, we get the following picture:

.. image:: ../_static/img/alcohol.svg
   :height: 480px
   :width: 480px
   :align: center
"""

from usainboltz import Atom, Epsilon, Generator, Grammar, MSet, RuleName

if __name__ == "__main__":
    carbon = Atom()
    A = RuleName("A")  # A for alcohol
    hydrogen = Epsilon()
    grammar = Grammar({A: hydrogen + carbon * MSet(A, eq=3)})

    generator = Generator(grammar)
    for _ in range(20):
        res = generator.sample((10, 20))
        print(res.sizes[carbon])

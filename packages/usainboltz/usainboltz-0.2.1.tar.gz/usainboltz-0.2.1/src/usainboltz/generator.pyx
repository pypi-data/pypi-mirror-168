# distutils: language = c++
# cython: language_level = 3

# Copyright 2019-2022 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

r"""Boltzmann generator for Context-free grammars.

This module provides functions for generating combinatorial objects (i.e.
objects described by a combinatorial specification, see
:mod:`usainboltz.grammar`) according to the Boltzmann
distribution.

Given an unlabelled combinatorial class A, the Boltzmann distribution of
parameter :math:`x` is such that an object of size n is drawn with the
probability :math:`\frac{x^n}{A(x)}` where :math:`A(x)` denotes the ordinary
generating function of A.  For labelled classes, this probability is set to
:math:`\frac{x^n}{n!A(x)}` where :math:`A(x)` denotes the exponential
generating function of A. See [DuFlLoSc04]_ for details.

By default, the objects produced by the generator are nested tuples of strings
(the atoms). For instance ``('z', ('z', 'epsilon', 'epsilon'), ('z', 'epsilon', 'epsilon'))`` is a
balanced binary tree with 3 internal nodes (z) and 4 leaves (e). To alter this
behaviour and generate other types of objects, you can specify a builder
function for each type of symbol in the grammar. The behaviour of the builders
is that they are applied in bottom up order to the structure "on the fly" during
generation. For instance, in order to generate Dyck words using the grammar for
binary trees, one can use a builder that return ``""`` for each leaf ``"(" +
left child + ")" + right child`` for each node. The builders will receive a
tuple for each product, a string for each atom and builders for unions should be
computed using the :func:`union_builder` helper. See the example below for the
case of Dyck words.

Examples:
    >>> from usainboltz import *
    >>> from usainboltz.generator import rng_seed
    >>> rng_seed(0xDEADBEEFCA7B0172)

    Both binary trees and Dyck words can be generated from the following
    grammar

    >>> epsilon, z, B = Epsilon(), Atom(), RuleName("B")
    >>> grammar = Grammar({B: epsilon + z * B * B})
    >>> generator = Generator(grammar, B, singular=True)

    In order to build Dyck words, one can interpret epsilon as the empty word
    and nodes as the derivation: ``D -> ( D ) D``

    >>> def leaf_builder(_):
    ...     return ""

    >>> def node_builder(tuple):
    ...     _, left, right = tuple
    ...     return "(" + left + ")" + right

    >>> generator.set_builder(B, union_builder(leaf_builder, node_builder))
    >>> res = generator.sample((10, 20))
    >>> dyck_word = res.obj
    >>> dyck_word
    '(())(((((()(((()())))))))())()'
    >>> len(dyck_word) in range(20, 41)
    True

    If on the contrary we want to see trees as S-expressions, we can interpret
    epsilon as the leaf ``"leaf"`` and nodes as ``(node left_child
    right_child)``

    >>> def leaf_builder(_):
    ...     return "leaf"

    >>> def node_builder(tuple):
    ...     _, left, right = tuple
    ...     return "(node {} {})".format(left, right)

    >>> generator.set_builder(B, union_builder(leaf_builder, node_builder))
    >>> res = generator.sample((10, 20))
    >>> print(res.obj)
    (node
      (node
        leaf
        (node
          leaf
          (node
            (node
              (node
                (node leaf leaf)
                leaf)
              (node
                (node
                    leaf
                    (node
                      (node
                        (node leaf leaf)
                        (node
                          (node
                            leaf
                            (node
                              (node leaf leaf)
                              leaf))
                          leaf))
                      leaf))
                leaf))
            (node
              (node leaf leaf)
              leaf))))
      leaf)

    Note that the builders mechanism can also be used to compute some
    statistics on the fly without explicitly building the whole structure. For
    instance the following example illustrates how to generate the **height**
    of a tree following the Boltzmann distribution without building the tree.

    >>> def leaf_height(_):
    ...     return 0

    >>> def node_height(tuple):
    ...     _, left, right = tuple
    ...     return 1 + max(left, right)

    >>> generator.set_builder(B, union_builder(leaf_height, node_height))
    >>> res = generator.sample((10, 20))
    >>> res.obj
    13
    >>> res.sizes[Atom()]
    16

For labelled grammar, the procedure is the same. In this case, the default
builders also output the labelling, they do not only generate the structure.

Example:
    >>> z = Atom()
    >>> e, M = Epsilon(), RuleName()
    >>> g = Grammar({M: e + z * M + z * M * M}, labelled=True)
    >>> generator = Generator(g, M, singular=True)
    >>> res = generator.sample((5,10))  # random
    >>> tree = res.obj
    >>> tree
    (4, (5, (0, (6, (3, (7, (1, 'epsilon', 'epsilon'), 'epsilon'), 'epsilon')), (2, 'epsilon', 'epsilon')), 'epsilon'))

"""

from libc.math cimport exp
from libc.stdint cimport uint64_t
from libcpp.pair cimport pair
from libcpp.stack cimport stack
from libcpp.vector cimport vector

import copy
from collections import namedtuple

from usainboltz.grammar import (
    Atom,
    Epsilon,
    Marker,
    MSet,
    Product,
    RuleName,
    Seq,
    Set,
    Union,
)
from usainboltz.oracle import build_oracle

from usainboltz.cpp_simulator cimport (
    ATOM,
    EPSILON,
    MARKER,
    MSET,
    PRODUCT,
    REF,
    SEQ,
    SET,
    UNION,
    CRule,
    initial_partition,
    next_partition,
    rule_type,
)
from usainboltz.simulator cimport (
    Simulator,
    bounded_geometric,
    bounded_mset_distribution,
    bounded_poisson,
    rng_double,
    rng_get_state,
    rng_i64,
    rng_seed as _rng_seed,
    rng_set_state,
)


# XXX. Is this indirection necessary?
cpdef void rng_seed(uint64_t s):
    _rng_seed(s)


# ------------------------------------------------------- #
# Grammar preprocessing
# ------------------------------------------------------- #

# For performance reasons, we use integers rather that strings to identify
# symbols during generation.
# The Mapping class computes a mapping from integers to rule names, a mapping from
# integers to markers, and their inverse mappings.
#
# All of this should remain hidden from the end user.

class Mapping:
    def __init__(self, grammar):
        # Rule names
        rule_name_to_id, id_to_rule_name = self._make_mapping(grammar.rules.keys())
        self.rule_name_to_id = rule_name_to_id
        self.id_to_rule_name = [id_to_rule_name[i] for i in range(len(id_to_rule_name))]
        # Markers
        marker_to_id, id_to_marker = self._make_mapping(grammar.markers())
        self.marker_to_id = marker_to_id
        self.id_to_marker = [id_to_marker[i] for i in range(len(id_to_marker))]

    def nb_rules(self):
        return len(self.id_to_rule_name)

    def nb_markers(self):
        return len(self.id_to_marker)

    @staticmethod
    def _make_mapping(iterable, start=0):
        x_to_id = {}
        id_to_x = {}
        for i, x in enumerate(iterable, start=start):
            x_to_id[x] = i
            id_to_x[i] = x
        return x_to_id, id_to_x


# ------------------------------------------------------- #
# Generic builders
# ------------------------------------------------------- #

# When it chooses one possible derivation for a union rule, the random
# generator wraps the generated object in a tuple of the form ``(choice_id,
# object)`` so that the builder that will be called on this value has the
# information of which derivation was chosen. This helper function hides this
# machinery to the end user, allowing her to compose builders in a "high-level"
# manner.

def union_builder(*builders):
    """Factory for generating builders for union rules.

    The recommended way to write a builder for a union rule is to use this
    helper: write a auxilliary builder for each component of the union and
    compose them with ``union_builder``.

    Args:
        builders (List[function]): builder functions, one for each component of
            the union.

    Returns:
        function: a builder function for a disjoint union. The resulting
            function applies one of the functions passed as arguments to its
            input depending of the component of the union its argument belongs
            to.

    Examples:
        Assume the symbol ``D`` is defined by ``Union(A, B, C)``, then
        defining a builder for D looks like:

        >>> def build_A(args):
        ...     # Do something
        ...     pass

        >>> def build_B(args):
        ...     # Do something
        ...     pass

        >>> def build_C(args):
        ...     # Do something
        ...     pass

        >>> build_D = union_builder(build_A, build_B, build_C)

        For instance, for binary trees defined by ``B = Union(leaf, Product(z,
        B, B))``, this could be:

        >>> def build_leaf(_):
        ...     return BinaryTree()

        >>> def build_node(args):
        ...     z, left, right = args
        ...     return BinaryTree([left, right])

        >>> build_binarytree = union_builder(build_leaf, build_node)

    """
    def build(obj):
        index, content = obj
        builder = builders[index]
        return builder(content)
    return build

# The following functions generate the default builders for labelled and
# unlabelled structures. These builders produce nested tuples. Choices ids are
# omitted for readability.

cdef inline identity(x):
    return x

cdef inline ProductBuilder(builders):
    def build(terms):
        return tuple([builders[i](terms[i]) for i in range(len(terms))])
    return build

cdef inline SeqBuilder(builder):
    def build(terms):
        return [builder(term) for term in terms]
    return build

cdef make_default_builder(rule):
    """Generate the default builders for a rule.

    Args:
        rule (Rule): a grammar rule.

    Returns:
        function: a simple builder for the rule passed as argument that
            generate objects as nested tuples.
    """
    # Symbols
    if isinstance(rule, RuleName):
        return identity
    elif isinstance(rule, (Atom, Marker, Epsilon)):
        return identity
    # Grammar combinators
    elif isinstance(rule, Product):
        subbuilders = [make_default_builder(component) for component in rule.args]
        return ProductBuilder(subbuilders)
    elif isinstance(rule, Seq):
        subbuilder = make_default_builder(rule.arg)
        return SeqBuilder(subbuilder)
    elif isinstance(rule, Set):
        subbuilder = make_default_builder(rule.arg)
        # Same as Seq
        return SeqBuilder(subbuilder)
    elif isinstance(rule, MSet):
        subbuilder = make_default_builder(rule.arg)
        # Same as Seq
        return SeqBuilder(subbuilder)
    elif isinstance(rule, Union):
        subbuilders = [make_default_builder(component) for component in rule.args]
        return union_builder(*subbuilders)
    else:
        raise NotImplementedError("make_default_builder({})".format(type(rule)))


# ------------------------------------------------------- #
# Random generation
# ------------------------------------------------------- #

# The generator is implemented as a stack machine.
# This stack machine has more instructions that the simulator because
# it also has to build a data structure. We thus split its instructions
# into two kinds:
# - generation instructions describe what to sample (as in the simulator);
# - build instructions describe how to construct the data structure that will be
#   returned to the user.

# Special instructions used by the random generators.
# They all take an integer argument.
ctypedef enum build_instr_name:
    TUPLE,       # Wrap the topmost k elements of the generated stack in a tuple
    LIST,        # Wrap the topmost k elements of the generated stack in a list
    FUNCTION,    # Call the k-th builder on the top of the stack
    WRAP_CHOICE  # Wrap the top element (x) of stack as a pair (k, x)
    MULTIPLICITY # Update the value of the `multiplicity` register of the state machine
    DUPLICATE    # Duplicate the last generated structure several times

# A build instruction and its integer argument
ctypedef struct build_instr:
    build_instr_name name
    int payload

# Union of the two kinds of instructions
ctypedef union instruction_desc:
    build_instr as_build_instr  # Build instruction
    const CRule *as_gen_instr   # Generation instruction (just the rule to generate)

# The instruction type
ctypedef struct instruction:
    bint is_gen_instr
    instruction_desc desc

cdef instruction make_gen_instr(const CRule *rule):
    cdef instruction instruction
    instruction.is_gen_instr = True
    instruction.desc.as_gen_instr = rule
    return instruction

cdef instruction make_build_instr(build_instr_name name, int payload):
    cdef instruction instruction
    instruction.is_gen_instr = False
    instruction.desc.as_build_instr.name = name
    instruction.desc.as_build_instr.payload = payload
    return instruction

# Free Boltzmann sampler (actual generation) of *unlabelled* structures.
# Does not handle the labelling of labelled structures

cdef c_generate(const CRule *first_rule, list builders, list marker_names, list labels):
    cdef list generated = []      # Stack of generated structures
    cdef stack[instruction] todo  # Stack of instructions

    cdef instruction current  # Current instruction
    cdef const CRule* rule    # The next rule to generate (when current.is_gen_instr)
    cdef build_instr instr    # The next build step (when not current.is_gen_instr)

    # A bunch of (many too many?) temporary variables.
    cdef instruction arg_instr
    cdef const CRule* arg
    cdef vector[CRule*] args
    cdef vector[vector[double]] weights
    cdef double r
    cdef unsigned int i = 0, k, multiplicity = 1
    cdef int lower_size, upper_size
    cdef vector[pair[int, int]] partition

    # Pre compute some instructions
    cdef vector[instruction] build_instructions;
    for i in range(len(builders)):
        build_instructions.push_back(make_build_instr(FUNCTION, i))

    # Initialise the stack machine with the first instruction to generate
    todo.push(make_gen_instr(first_rule))

    while not todo.empty():
        current = todo.top()
        todo.pop()
        # Handling of the random generation instructions.
        if current.is_gen_instr:
            rule = current.desc.as_gen_instr
            # Symbols
            if rule.get_type() == EPSILON:
                generated.append("epsilon")
            elif rule.get_type() == ATOM:
                if labels is not None:
                    generated.append(labels.pop())
                else:
                    generated.append("z")
            elif rule.get_type() == MARKER:
                generated.append(marker_names[rule.get_marker_id()])
            elif rule.get_type() == REF:
                todo.push(build_instructions[rule.get_ref_id()])
                todo.push(make_gen_instr(rule.get_ref_rule()))
            # Grammar combinators
            elif rule.get_type() == UNION:
                r = rng_double()
                i = 0
                args = rule.get_union_args()
                weights = rule.get_union_weights()
                while i < args.size():
                    r -= weights[i][multiplicity]
                    if r <= 0:
                        todo.push(make_build_instr(WRAP_CHOICE, i))
                        todo.push(make_gen_instr(args[i]))
                        break
                    i += 1
            elif rule.get_type() == PRODUCT:
                args = rule.get_product_args()
                todo.push(make_build_instr(TUPLE, args.size()))
                for arg in args:
                    todo.push(make_gen_instr(arg))
            elif rule.get_type() == SEQ:
                k = bounded_geometric(
                    1.0 - rule.get_iter_arg_weight()[multiplicity],
                    rule.get_iter_lower_size(),
                    rule.get_iter_upper_size()
                )
                todo.push(make_build_instr(LIST, k))
                arg_instr = make_gen_instr(rule.get_iter_arg())
                for i in range(k):
                    todo.push(arg_instr)
            elif rule.get_type() == SET:
                arg = rule.get_iter_arg()
                k = bounded_poisson(
                    rule.get_iter_weight()[multiplicity],
                    rule.get_iter_arg_weight()[multiplicity],
                    rule.get_iter_lower_size(),
                    rule.get_iter_upper_size()
                )
                # store sets as lists
                todo.push(make_build_instr(LIST, k))
                arg_instr = make_gen_instr(arg)
                for i in range(k):
                    todo.push(arg_instr)
            elif rule.get_type() == MSET:
                lower_size = rule.get_iter_lower_size()
                upper_size = rule.get_iter_upper_size()

                # Save the current multiplicity
                todo.push(make_build_instr(MULTIPLICITY, multiplicity))

                # List of the recursive calls to make (with multiplicity)
                mults = []

                if upper_size >= 0:
                    if lower_size < upper_size:
                        raise NotImplementedError("MSet with bounds other than `eq=`")

                    # Draw a partition under the distribution induced by their weights:
                    partition = initial_partition(lower_size)
                    r = rng_double() * rule.get_iter_weight()[multiplicity];
                    weights = rule.get_mset_partitions_weight()
                    for pw in weights:
                        r -= pw[multiplicity]
                        if r <= 0:
                            break
                        next_partition(partition)

                    # Set up the recursive calls for that partition:
                    for p in partition:
                        # Draw p.second independent elements with multiplicity p.first
                        mults.append((p.first, p.second))

                    # Instruct the generator to wrap the result as a list
                    todo.push(make_build_instr(LIST, lower_size))

                elif rule.get_iter_lower_size() > 0:
                    assert False

                else:
                    # Generate the number or arguments of each multiplicity
                    k = bounded_mset_distribution(
                        rule.get_iter_weight(),
                        rule.get_iter_arg_weight(),
                        multiplicity,
                    )
                    totsize = 0
                    for j in range(1, k):
                        # i ~ Poisson(A(z^{j m}) / j)
                        r = rule.get_iter_arg_weight()[j * multiplicity] / j
                        i = bounded_poisson(exp(r), r, 0, -1)
                        totsize += i * j * multiplicity
                        mults.append((j, i))
                    if k > 0:
                        # i ~ Poisson_{> 0}(A(z^{k m}) / k)
                        r = rule.get_iter_arg_weight()[k * multiplicity] / k
                        i = bounded_poisson(exp(r) - 1.0, r, 1, -1)
                        totsize += i * k
                        mults.append((k, i))

                    # Instruct the generator to wrap the result as a list
                    todo.push(make_build_instr(LIST, totsize))

                # Generate the generation intructions
                arg_instr = make_gen_instr(rule.get_iter_arg())
                for (j, nb) in mults:
                    # Generate i arguments with multiplicity `j * multiplicity`
                    for _ in range(nb):
                        # The generated structure should be duplicated j times
                        if j > 1:
                            todo.push(make_build_instr(DUPLICATE, j))
                        todo.push(arg_instr)
                    # the multiplicity used in the generating functions is j times the
                    # current multiplicity.
                    todo.push(make_build_instr(MULTIPLICITY, j * multiplicity))
            else:
                assert False
        # Handling of the build instructions.
        else:
            instr = current.desc.as_build_instr
            if instr.name == TUPLE:
                t = tuple(generated[:-instr.payload-1:-1])
                del generated[-instr.payload:]
                generated.append(t)
            elif instr.name == LIST:
                if instr.payload == 0:
                    generated.append([])
                else:
                    t = list(generated[-instr.payload:])
                    del generated[-instr.payload:]
                    generated.append(t)
            elif instr.name == FUNCTION:
                func = builders[instr.payload]
                x = generated.pop()
                generated.append(func(x))
            elif instr.name == WRAP_CHOICE:
                choice = generated.pop()
                generated.append((instr.payload, choice))
            elif instr.name == MULTIPLICITY:
                multiplicity = instr.payload
            elif instr.name == DUPLICATE:
                x = generated.pop()
                for _ in range(instr.payload):
                    generated.append(x)
            else:
                assert False

    obj, = generated
    return obj

cdef list _rand_perm(unsigned int n):
    """Draw an uniform random premutation of size ``n`` using the Fisher-Yates algorithm."""
    cdef unsigned int i, j
    cdef list p = list(range(0,n))

    for i in range(n-1,0,-1):
        j = rng_i64(i)
        p[i], p[j] = p[j], p[i]

    return p

cdef c_search_seed(simulator, first_rule, sizes_windows, labelling=False) except +:
    """Search for a tree in a given size window."""
    max_sizes = [size_max for (_, size_max) in sizes_windows]
    cdef uint64_t[4] backup_state

    # I'd need a do while
    rng_get_state(backup_state)

    sizes = simulator.run(first_rule, max_sizes)
    while not _in_sizes_windows(sizes, sizes_windows):
        # save the random generator's state
        rng_get_state(backup_state)
        sizes = simulator.run(first_rule, max_sizes)

    # Generate the labels BEFORE reseting the RNG
    labels = _rand_perm(sizes[0]) if labelling else None

    # Reset the random generator to the state it was just before the simulation
    rng_set_state(backup_state)
    return labels, sizes


# ------------------------------------------------------- #
# High level interface
# ------------------------------------------------------- #

cdef _in_sizes_windows(sizes, sizes_windows):
    for i, (size_min, size_max) in enumerate(sizes_windows):
        size = sizes[i]
        if size < size_min:
            return False
        if size_max > 0 and size > size_max:
            return False
    return True

class GeneratorConfigError(Exception):
    pass

Result = namedtuple("Result", ["obj", "sizes"])

class Generator:
    """High level interface for Boltzmann samplers."""

    def __init__(
        self,
        grammar,
        rule_name=None,
        singular=None,
        expectations=None,
        oracle=None
    ):
        """Make a Generator out of a grammar.

        Args:
            grammar (Grammar): a combinatorial grammar

            rule_name (RuleName): the rule name of the symbol to generate.

            singular (bool): if set, do singular sampling (use the
                singularity of the generating functions as parameter).

            expectations (Dict[Symbol,number]): this is passed to the oracle to
                skew the distribution in order to target some specific values
                for the expected number of the specified symbols. See
                :py:meth:`OracleFromPaganini.tuning` for more details.

            oracle (Oracle): an oracle for computing the values of some
                generating functions. If not supplied, a default generic oracle
                that should work for most use-cases is automatically generated.

        Examples:

        >>> from usainboltz import *

        Some examples using the grammar for binary trees
        >>> z, B = Atom(), RuleName()
        >>> grammar = Grammar({B: Epsilon() + z * B * B})

        Typical use:
        >>> generator = Generator(grammar, B, singular=True)

        Since their is only one symbol in the grammar, the second argument can be
        omitted:
        >>> generator = Generator(grammar, singular=True)

        """

        self.grammar = copy.deepcopy(grammar)
        self.rule_name = self._guess_rule_name(rule_name)
        # Map all symbols in the grammar to an integer identifier.
        # Use arrays rather than dictionaries.
        self.mapping = Mapping(grammar)
        # If `singular` and the expectations are unspecified, do singular sampling
        # by default.
        if singular is None:
            singular = not(bool(expectations))

        # Set up the oracle.
        oracle = oracle or build_oracle(self.grammar)
        self.oracle_values = oracle.tuning(
            rule=Atom() if singular else self.rule_name,
            expectations=expectations,
            singular=singular
        )

        self.sim = Simulator(self.grammar,
                             self.oracle_values,
                             self.mapping)


        # Initialise the default builders.
        self.builders = [
            make_default_builder(self.grammar.rules[self.mapping.id_to_rule_name[id]])
            for id in range(self.mapping.nb_rules())
        ]

    def _guess_rule_name(self, rule_name):
        if rule_name is not None:
            return rule_name
        rule_names = list(self.grammar.rules.keys())
        return rule_names[0]

    def _sanitize_windows(self, sizes_windows):
        if sizes_windows is None:
            sizes_windows = dict()
        elif isinstance(sizes_windows, tuple):
            sizes_windows = {Atom(): sizes_windows}
        return [
            sizes_windows.get(Atom(), (0, -1))
        ] + [
            sizes_windows.get(self.mapping.id_to_marker[i], (0, -1))
            for i in range(self.mapping.nb_markers())
        ]


    def set_builder(self, non_terminal, func):
        """Set the builder for a non-terminal symbol.

        Args:
            non_terminal (RuleName): the name of the non-terminal symbol.

            func (function): the builder.
        """
        symbol_id = self.mapping.rule_name_to_id[non_terminal]
        self.builders[symbol_id] = func

    def get_builder(self, non_terminal):
        """Retrieve the current builder for a non-terminal symbol.

        Args:
            non_terminal (RuleName): the name of the non-terminal symbol.

        Returns:
            function: the current builder currently bound to the rule name
                passed as argument.
        """
        symbol_id = self.mapping.rule_name_to_id[non_terminal]
        return self.builders[symbol_id]

    def _search_seed(self, sizes_windows):
        return c_search_seed(
            self.sim,
            self.rule_name,
            self._sanitize_windows(sizes_windows),
            self.grammar.labelled,
        )

    def _generate(self, labels):
        # This local variable is necessary for cython to see that self.sim is of type
        # Simulator.
        cdef Simulator sim = self.sim
        cdef CRule* start = sim.c_rules[self.mapping.rule_name_to_id[self.rule_name]]
        return c_generate(start, self.builders, self.mapping.id_to_marker, labels)

    def sample(self, sizes_windows):
        """Generate a term of the grammar given the prescribed sizes.

        Args:
            sizes_windows (Tuple[int,int]] | Dict[(Atom|Marker),Tuple[int,int]]):
                for atoms (resp. markers) for which a size window is
                specified, the generator will only generate objects whose
                number of those atoms (resp. markers) are in the
                specified size windows. For instance a
                ``generator.sample({z: (100, 200)})`` will only generate
                objects with a number of ``z`` belonging to the
                interval `[100, 200]`.
        """
        labels, sizes = self._search_seed(sizes_windows)
        res = self._generate(labels)
        ret_sizes = {
            self.mapping.id_to_marker[i]: sizes[i+1] for i in range(len(sizes)-1)
        }
        ret_sizes[Atom()] = sizes[0]
        return Result(obj=res, sizes=ret_sizes)

# coding: utf-8

# Copyright 2019-2022 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

r"""
Context-free grammars for Boltzmann generation.
===============================================

Grammars use the basic operators of the symbolic method of analytic
combinatorics to specify labelled or unlabelled combinatorial classes. For
instance, binary trees can be specified by ``B = leaf + Z * B * B`` which,
using the syntax implemented in this module, looks like:

Examples:
    >>> z, leaf = Atom(), Marker("leaf")
    >>> B = RuleName("B")

    >>> # Using the explicit syntax
    >>> Grammar({B: Union(leaf, Product(z, B, B))})
    {
      B : Union(leaf, Product(z, B, B))
    }
    >>> # Using the syntactic sugar + and * for unions and products
    >>> Grammar({B: leaf + z * B * B})
    {
      B : Union(leaf, Product(z, B, B))
    }


Note that we make the difference between

- terminal symbols of the grammar: :py:class:`Atom` (``leaf`` and ``z`` in the
  above example).
- non-terminal symbols: :py:class:`RuleName` (``B`` in the above example).

The most basic constructions of the symbolic method are the Cartesian product
:py:class:`Product` and the disjoint union :py:class:`Union`. In the example of
binary trees, disjoint union is used to decompose the class between leaves and
internal nodes. The Cartesian product is used to define internal nodes as a
pair of children, the ``z`` appearing at each internal node means that each
node counts as :math:`1` in the size of a tree.

The exhaustive list of supported constructions is given below. Detailed
explanations about each of these operators can be found on the `Wikipedia page
<https://en.wikipedia.org/wiki/Symbolic_method_(combinatorics)>`_ of the
symbolic method and in [FS2009]_.

Here are two other examples of specifications, for general plane trees,
illustrating the use of the :class:`Seq` (sequence) operator and the use of
multi-rules grammars:

Examples:
    >>> z = Atom()
    >>> T, S = RuleName("T"), RuleName("S")

    >>> # With Seq
    >>> Grammar({T: z * Seq(T)})
    {
      T : Product(z, Seq(T))
    }

    >>> # Equivalent definition without Seq
    >>> nil = Epsilon()
    >>> Grammar({
    ...     T: z * S,
    ...     S: nil + T * S,
    ... })
    {
      S : Union(epsilon, Product(T, S)),
      T : Product(z, S)
    }

.. todo:: Write about labeling

AUTHORS:

- Matthieu Dien (2019): initial version

- Martin Pépin (2019): initial version

.. rubric:: References

.. [FS2009] Philippe Flajolet, Robert Sedgewick, 2009, Analytic combinatorics,
   Cambridge University Press.
"""

from functools import reduce
from typing import Dict, List, Optional, Set as PythonSet, Union as TypeUnion

__all__ = (
    "Marker",
    "Epsilon",
    "Atom",
    "Cycle",
    "Grammar",
    "MSet",
    "Product",
    "RuleName",
    "Seq",
    "Set",
    "Union",
    "UCycle",
)


# ------------------------------------------------------- #
# Fresh names generation
# ------------------------------------------------------- #


class _NameGenerator:
    def __init__(self, prefix: str):
        self.prefix = prefix
        self.counter = 0

    def fresh(self) -> str:
        fresh_name = "{}_{}".format(self.prefix, self.counter)
        self.counter += 1
        return fresh_name


_symbol_name_generator = _NameGenerator("_symbol")


# ------------------------------------------------------- #
# Grammar implementation
# ------------------------------------------------------- #


class Rule:
    """The super class of all grammar rules.

    Should not be instantiated directly.
    """

    def markers(self) -> PythonSet["Marker"]:
        raise NotImplementedError("Sub classes of Rule should implement self.markers()")

    def __add__(self, rhs: "Rule") -> "Rule":
        """Disjoint union of rules using the + syntax.

        Examples:
            >>> a, b, c, d = Marker("a"), Marker("b"), Marker("c"), Marker("d")

            >>> a + b
            Union(a, b)

            >>> Union(a, b) + c
            Union(a, b, c)

            >>> a + Union(b, c)
            Union(a, b, c)

            >>> Union(a, b) + Union(c, d)
            Union(a, b, c, d)
        """
        # ensure not to build unions of unions
        lhs_terms = self.args if isinstance(self, Union) else [self]
        rhs_terms = rhs.args if isinstance(rhs, Union) else [rhs]
        return Union(*(lhs_terms + rhs_terms))

    def __mul__(self, rhs: "Rule") -> "Rule":
        """Cartesian product of rules using the * syntax.

        Examples:
            >>> a, b, c, d = Marker("a"), Marker("b"), Marker("c"), Marker("d")

            >>> a * b
            Product(a, b)

            >>> Product(a, b) * c
            Product(a, b, c)

            >>> a * Product(b, c)
            Product(a, b, c)

            >>> Product(a, b) * Product(c, d)
            Product(a, b, c, d)
        """
        # ensure not to build products of products
        # ensure not to build unions of unions
        lhs_terms = self.args if isinstance(self, Product) else [self]
        rhs_terms = rhs.args if isinstance(rhs, Product) else [rhs]
        return Product(*(lhs_terms + rhs_terms))

    def __pow__(self, n: int) -> "Rule":
        """Exponentiation using the ** syntax.

        Examples:
            >>> A = RuleName("A")
            >>> A ** 3
            Product(A, A, A)

            >>> A ** 1
            A

            >>> A ** 0
            epsilon
        """
        if n < 0:
            raise ValueError("Exponentiation to a negative integer is forbidden.")
        elif n == 0:
            return Epsilon()
        elif n == 1:
            return self
        else:
            return Product(*[self for _ in range(n)])

    def __xor__(self, n: int) -> "Rule":
        """Exponentiation using the ^ syntax.

        Examples:
            >>> A = RuleName("A")
            >>> A ^ 3
            Product(A, A, A)

            >>> A ^ 1
            A

            >>> A ^ 0
            epsilon
        """
        return self**n


class IteratedRule(Rule):
    """The base class for iterated constructions Seq, Set, Cycle, MSet, etc.

    Should not be instantiated directly.
    """

    # This class attribute is used for pretty-printing. It has to be set in
    # classes extending IteratedRule.
    construction_name: str

    def __init__(
        self,
        arg: TypeUnion[Rule, str],
        leq: Optional[int] = None,
        geq: Optional[int] = None,
        eq: Optional[int] = None,
    ):
        """Rule constructor.

        Args:
          arg: a rule describing the elements of the
            collection.

          leq: constrains the collection to have size at most ``leq``.

          geq: constrains the collection to have size at least ``geq``.

          eq: constrains the collection to have size exactly ``eq``.
        """
        super(IteratedRule, self).__init__()

        assert leq is None or geq is None or geq <= leq
        assert eq is None or (leq is None and geq is None)  # eq != 0 => leq == geq == 0

        self.lower_size = None
        self.upper_size = None

        if eq is not None:
            self.lower_size = eq
            self.upper_size = eq
        else:
            self.lower_size = geq
            self.upper_size = leq

        self.arg = _to_rule(arg)

    def __repr__(self) -> str:
        if self.construction_name is None:
            raise ValueError("IteratedRule should not be used directly!")
        constraint = ""
        if self.lower_size is not None:
            if self.lower_size == self.upper_size:
                constraint = ", eq = {}".format(self.upper_size)
                return "{}({}{})".format(self.construction_name, self.arg, constraint)
            else:
                constraint += ", geq = {}".format(self.lower_size)
        if self.upper_size is not None:
            constraint += ", leq = {}".format(self.upper_size)
        return "{}({}{})".format(self.construction_name, self.arg, constraint)

    def markers(self) -> PythonSet["Marker"]:
        """Return the set of all markers in the rule."""
        return self.arg.markers()


class Symbol(Rule):
    """Base class for all grammar symbols (Atom, RuleName, Epsilon).

    Should not be instantiated directly.
    """

    def __init__(self, name: Optional[str] = None):
        super(Symbol, self).__init__()
        if name is None:
            name = _symbol_name_generator.fresh()
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Symbol) and self.name == other.name

    def __lt__(self, other: Rule) -> bool:
        if not isinstance(other, Symbol):
            raise TypeError("Cannot compare Symbol and {}".format(type(other)))
        return self.name < other.name

    def markers(self) -> PythonSet["Marker"]:
        """Return the set of all markers contained in the expression."""
        return set()


class Marker(Symbol):
    """Marker symbols.

    Examples:
        >>> Marker("u")
        u

        >>> Marker()
        _symbol_0

    Markers are similar to atoms but have size 0. They are usually used to
    mark some special places in the grammar. For instance in the following
    grammar for Motzkin tree, the marker `u` is used to mark unary nodes.

    Examples:
        >>> z, u, M = Atom(), Marker(), RuleName()
        >>> grammar = Grammar({M: z + u * z * M + z * M * M})
    """

    def markers(self) -> PythonSet["Marker"]:
        return {self}


class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance


class Epsilon(Singleton, Symbol):
    """The epsilon symbol.

    Epsilon is the class containing only one element of size 0.

    Note:
        There is only one instance of the Epsilon class.

    Examples:
        >>> eps1 = Epsilon()
        >>> eps2 = Epsilon()
        >>> eps1 is eps2
        True
    """

    def __init__(self):
        super(Epsilon, self).__init__("epsilon")


class Atom(Singleton, Symbol):
    """Terminal symbol of a grammar, accounts for the size.

    Atom is the class containing only one element of size 1.

    Note:
        There is only one instance of the Atom class.

    >>> Atom()
    z

    >>> Atom() is Atom()
    True
    """

    def __init__(self):
        super(Atom, self).__init__("z")


class RuleName(Symbol):
    """Non terminal symbols of a grammar.

    Instances of this class represent recursive references to non-terminal
    symbols inside grammar rules. For instance, sequences of atoms ``z`` could
    be defined using the following grammar where the :py:class:`RuleName` ``S``
    refers to itself in its definition:

    Examples:
        >>> epsilon, z, S = Epsilon(), Atom(), RuleName("S")
        >>> Grammar({S: epsilon + z * S})
        {
            S : Union(epsilon, Product(z, S))
        }
    """


def _to_rule(rule: TypeUnion[str, Rule]) -> Rule:
    """Cast strings to RuleNames, otherwise do nothing."""
    if isinstance(rule, Rule):
        return rule
    elif isinstance(rule, str):
        return RuleName(rule)
    else:
        raise ValueError("_to_rule accepts only rules and strings")


def _to_rulename(rule_name: TypeUnion[str, RuleName]) -> RuleName:
    """Cast strings to RuleNames, otherwise do nothing."""
    if isinstance(rule_name, RuleName):
        return rule_name
    elif isinstance(rule_name, str):
        return RuleName(rule_name)
    else:
        raise ValueError("_to_rulename accepts only RuleNames and strings")


class Union(Rule):
    """Disjoint union of two or more rules.

    ``D = Union(A, B, C)`` corresponds to the following grammar in BNF syntax:
    ``D ::= A | B | C``

    Examples:
        >>> A, B, C = RuleName("A"), RuleName("B"), RuleName("C")

        >>> Union(A, B, C)
        Union(A, B, C)

        >>> z = Atom()
        >>> Union(z, A)
        Union(z, A)
    """

    args: List[Rule]

    def __init__(self, *terms: TypeUnion[Rule, str]):
        """Build a union of two or more rules.

        Args:
            terms: list of terms of the union.
        """
        super(Union, self).__init__()

        if len(terms) < 2:
            raise ValueError("Unions should have at least two terms")
        self.args = [_to_rule(arg) for arg in terms]

    def __repr__(self) -> str:
        return "Union({})".format(", ".join(map(repr, self.args)))

    def markers(self) -> PythonSet[Marker]:
        """Return the set of markers contained in the expression."""
        return reduce(lambda x, y: x | y, (arg.markers() for arg in self.args))


class Product(Rule):
    """Cartesian product of two or more rules.

    ``Product(A, B, C)`` corresponds to the following grammar in BNF syntax:
    ``_ ::= A × B × C``

    Examples:
        >>> A, B, C = RuleName("A"), RuleName("B"), RuleName("C")

        >>> Product(A, B, C)
        Product(A, B, C)

        >>> z = Atom()
        >>> Product(z, A)
        Product(z, A)
    """

    args: List[Rule]

    def __init__(self, *factors: TypeUnion[Rule, str]):
        """Build the product of two or more rules.

        Args:
            factors: list of factors of the product.
        """
        super(Product, self).__init__()
        if len(factors) < 2:
            raise ValueError("Products should have at least two components")
        self.args = [_to_rule(arg) for arg in factors]

    def __repr__(self) -> str:
        return "Product({})".format(", ".join(map(repr, self.args)))

    def markers(self) -> PythonSet[Marker]:
        """Return the set of all markers contained in the expression."""
        return reduce(lambda x, y: x | y, (arg.markers() for arg in self.args))


class Seq(IteratedRule):
    """Sequences.

    The Seq construction of the symbolic method models sequences of elements.
    In the following example, Seq is used to represent binary words as
    sequences of bits.

    Example:
        >>> z, one, zero, S = Atom(), Marker("1"), Marker("0"), RuleName("S")
        >>> Grammar({S: Seq(z * (one + zero))})
        {
          S : Seq(Product(z, Union(1, 0)))
        }

    The number of terms of a sequence can be constrained to be greater or
    smaller that some integer constants:

    Examples:
        >>> z, one, zero = Atom(), Marker("1"), Marker("0")

        >>> Seq(z * (one + zero), leq=10, geq=5)
        Seq(Product(z, Union(1, 0)), geq = 5, leq = 10)

        >>> Seq(z * (one + zero), leq=10)
        Seq(Product(z, Union(1, 0)), leq = 10)

        >>> Seq(z * (one + zero), geq=5)
        Seq(Product(z, Union(1, 0)), geq = 5)
    """

    construction_name = "Seq"  # For pretty-printing.


class Set(IteratedRule):
    """Labelled sets.

    The labelled Set construction of the symbolic method models sets of
    elements. In the following example, Set is used to model labelled general
    trees.

    Example:
        >>> z, T = Atom(), RuleName("T")
        >>> Grammar({T: z * Set(T)})
        {
          T : Product(z, Set(T))
        }

    The number of elements of the set can be constrained to be greater or
    smaller that some integer constants:

    Examples:
        >>> z = Atom()

        >>> # sets of 5 to 10 elements
        >>> Set(z, geq=5, leq=10)
        Set(z,  geq = 5, leq = 10)

        >>> # sets of at least 5 elements
        >>> Set(z, geq = 5)
        Set(z, geq = 5)

        >>> # sets of at most 10 elements
        >>> Set(z, leq=10)
        Set(z, leq = 10)
    """

    construction_name = "Set"  # For pretty-printing.


class Cycle(IteratedRule):
    """Labelled cycles.

    A cycle is like a sequence whose components can be cyclically shifted. For
    instance: [a, b, c], [b, c, a] and [c, a, b] represent the same cycle. In
    the following example, Cycle is used to represent the class of permutations
    as a set of cycles:

    Example:
        >>> z, P = Atom(), RuleName("P")
        >>> Grammar({P: Set(Cycle(z))})
        {
          P : Set(Cycle(z))
        }

    The number of elements of the cycle can be constrained to be greater or
    smaller that some integer constants:

    Examples:
        >>> z = Atom()

        >>> Cycle(z, geq=5, leq=10)
        Cycle(z, geq = 5, leq = 10)

        >>> Cycle(z, geq=5)
        Cycle(z, geq = 5)

        >>> Cycle(z, leq=10)
        Cycle(z, leq = 10)
    """

    construction_name = "Cycle"

    def __init__(
        self,
        arg: TypeUnion[Rule, str],
        leq: Optional[int] = None,
        geq: Optional[int] = None,
        eq: Optional[int] = None,
    ):
        if leq == 0 or geq == 0:
            raise ValueError("Cycles should contain at least one component")
        super(Cycle, self).__init__(arg, leq, geq, eq)


class MSet(IteratedRule):
    """Unlabelled multi-sets.

    A multi-set is like a set where elements can occur multiple times. In the
    following example, MSet is used to represent the class of non-plane
    general trees:

    Examples:
        >>> z, T = Atom(), RuleName("T")
        >>> Grammar({T: z * MSet(T)})
        {
          T : Product(z, MSet(T))
        }

    The number of elements of the multi-set can be constrained to be greater or
    smaller that some integer constants:

    Examples:
        >>> z = Atom()

        >>> MSet(z, geq=5, leq=10)
        MSet(z, geq = 5, leq = 10)

        >>> MSet(z, geq=5)
        MSet(z, geq = 5)

        >>> MSet(z, leq=10)
        MSet(z, leq = 10)
    """

    construction_name = "MSet"  # For pretty-printing.


class UCycle(IteratedRule):
    """Unlabelled cycles.

    A cycle is like a sequence whose components can be cyclically shifted. For
    instance: [a, b, c], [b, c, a] and [c, a, b] represent the same cycle.

    The number of elements of the cycle can be constrained to be greater or
    smaller that some integer constants:

    Examples:
        >>> z = Atom()

        >>> UCycle(z, geq=5, leq=10)
        UCycle(z, geq = 5, leq = 10)

        >>> UCycle(z, geq=5)
        UCycle(z, geq = 5)

        >>> UCycle(z, leq=10)
        UCycle(z, leq = 10)
    """

    construction_name = "UCycle"  # For pretty-printing

    def __init__(
        self,
        arg: TypeUnion[Rule, str],
        leq: Optional[int] = None,
        geq: Optional[int] = None,
        eq: Optional[int] = None,
    ):
        if leq == 0 or geq == 0:
            raise ValueError("UCycles should contain at least one component")
        super(UCycle, self).__init__(arg, leq, geq, eq)


class Grammar:
    """Context free grammars."""

    rules: Dict[RuleName, Rule]

    def __init__(
        self,
        rules: Optional[Dict[RuleName, Rule]] = None,
        labelled: bool = False,
    ):
        r"""Create a grammar.

        The rules of the grammar can be either specified at grammar creation by
        feeding them to the constructor or specified later using the
        :py:meth:`add_rule` method.

        Args:
          rules: dictionary mapping RuleNames to Rules

        Examples:
            >>> z = Atom()

            The grammar of sequences

            >>> S = RuleName("S")
            >>> Grammar({S: Epsilon() + z * S})
            {
              S : Union(epsilon, Product(z, S))
            }

            The grammar of binary trees

            >>> B = RuleName("B")
            >>> Grammar({B: Epsilon() + z * B * B})
            {
              B : Union(epsilon, Product(z, B, B))
            }

            The grammar of unary-binary trees (or Motzkin trees)

            >>> g = Grammar()
            >>> T, U, B = RuleName("T"), RuleName("U"), RuleName("B")
            >>> g.add_rule(T, z + U + B)
            >>> g.add_rule(U, z * T)
            >>> g.add_rule(B, z * T * T)
            >>> g
            {
              B : Product(z, T, T),
              T : Union(z, U, B),
              U : Product(z, T)
            }
        """
        self.rules = {}
        rules = rules or {}
        # Pass the dictionary of rules to the add_rule method, add_rule does
        # all the sanitizing work
        for name, rule in rules.items():
            self.add_rule(name, rule)
        self.labelled = labelled

    def add_rule(
        self, rule_name: TypeUnion[RuleName, str], rule: TypeUnion[Rule, str]
    ) -> None:
        """Add a rule to the grammar.

        Args:
            rule_name: a non-terminal symbol. If it was already defined in the grammar,
                it is replaced.

            rule: the rule defining ``rule_name``.

        Examples:
            >>> A, B, C = RuleName("A"), RuleName("B"), RuleName("C")
            >>> g = Grammar()
            >>> g.add_rule(A, Union(B, C))
            >>> g.rules[A]
            Union(B, C)
        """
        self.rules[_to_rulename(rule_name)] = _to_rule(rule)

    def __repr__(self) -> str:
        return (
            "{\n"
            + ",\n".join(
                "  {} : {}".format(non_terminal, expr)
                for non_terminal, expr in sorted(self.rules.items())
            )
            + "\n}"
        )

    def markers(self) -> PythonSet[Marker]:
        """Return all the markers appearing in the grammar.

        Examples:
            >>> z, u = Atom(), Marker("u")
            >>> B = RuleName("B")
            >>> g = Grammar({B: Union(u, Product(z, B, B))})
            >>> g.markers() == {u}
            True
        """
        return reduce(
            lambda x, y: x | y, (expr.markers() for expr in self.rules.values())
        )

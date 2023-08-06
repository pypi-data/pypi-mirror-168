# coding: utf-8

# Copyright 2019-2022 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

"""
Various oracle implementations for Boltzmann sampling.

Oracles are used to get (often approximate) values of generating functions.
Thanks to the symbolic method, functional equations can be derived from
grammar specifications. This module implements some mechanics to approximate
generating functions based on these equations.

Currently three oracles are implemented:

- :class:`OracleFromDict` does nothing. It takes a dictionary of already computed
  values from the user and wraps them as an :class:`Oracle`.
  This dictionary must have all the :class:`~usainboltz.grammar.Symbol`s of the grammar
  as keys and must be of one of the two following form:
  - Either it maps the symbols of the grammar to floating point values, in which
    case these values are interpreted as the values of the corresponding generating
    functions at a common point `z`.
  - Or it maps them to an array of floating point values, in which case the `j`-th
    entry of each array is interpreted as the value of the corresponding generating
    function at `z^j`.
- :class:`OracleFromPaganini` use the oracle Pagagnini of [BBD2018]_
- :class:`OracleFromNewtonGF` use the oracle NewtonGF of [PSS2012]_
  (only when Sagemath and Maple installations are present)

The entry point of these algorithms is the function oracle which determines
the oracle to use given its inputs.

AUTHORS:
- Matthieu Dien (2019): initial version
- Martin Pépin (2019): initial version

.. rubric:: References

.. [BBD2018] Maciej Bendkowski, Olivier Bodini, Sergey Dovgal, 2018,
   Polynomial tuning of multiparametric combinatorial samplers, ANALCO
.. [PSS2012] Carine Pivoteau, Bruno Salvy, Michèle Soria, 2012
   Algorithms for Combinatorial Structures: Well-founded systems and
   Newton iterations, Journal of Combinatorial Theory
"""

import sys
from functools import partial, reduce
from typing import Callable, Dict, List, NamedTuple, Optional, Tuple, Union as TypeUnion

import paganini as pg
from cvxpy import SolverError

from usainboltz.grammar import (
    Atom,
    Cycle,
    Epsilon,
    Grammar,
    Marker,
    MSet,
    Product,
    Rule,
    RuleName,
    Seq,
    Set,
    Symbol,
    UCycle,
    Union,
)

__all__ = ["build_oracle", "OracleFromPaganini", "OracleFromDict"]


class Oracle:
    """The super class of all oracles.

    Should not be instantiated directly.

    The ``tuning`` method must compute a suitable z and the corresponding values of the
    generating functions of the system.
    Sub classes may implement any interface for the tuning method as long as their
    output ``d`` satisfy the following requirements:

    - ``d[Atom()]`` is the list ``[1, z, z**2, z**3, ..., z**k]`` for some
      floating point value ``z`` et some positive integer ``k``;
    - for each symbol ``S`` of the grammar, ``d[S]`` is the list
      ``[1, S(z), S(z**2), S(z**3), ..., S(z**k)]`` where ``S(z**j)`` denotes the
      generating function for ``S`` (ordinary or exponential depending on the
      context) evaluated at ``z**j``;
    - all the lists appearing in this dictionary should have the same length
      (``k+1``).

    Most of the time ``k=1`` is enough but when Pólya operators like
    :py:class:`~usainboltz.grammar.MSet` appear in the grammar, more values are
    necessary.
    In such situations, any generation function ``S(z**j)`` with ``j > k`` will be
    approximated by zero.
    """

    tuning: Callable[..., Dict[Symbol, List[float]]]


def build_oracle(sys, **kargs) -> Oracle:
    """Build different oracles given different inputs

    EXAMPLES::
        >>> from usainboltz import *

        >>> leaf, z = Marker("leaf"), Atom()
        >>> B = RuleName("B")
        >>> g = Grammar({B: leaf + z * B * B})
        >>> build_oracle(g)
        OracleFromPaganini({
          B : Union(leaf, Product(z, B, B))
        })

        >>> build_oracle({'B': 2, 'z': 1./4})
        OracleFromDict({'B': [1.0, 2], 'z': [1.0, 0.25]})
    """

    if isinstance(sys, Grammar):
        return OracleFromPaganini(sys)
    elif isinstance(sys, dict):
        return OracleFromDict(sys)

    raise TypeError(
        "I do not know what to do with a system of type {}".format(type(sys))
    )


# ------------------------------------------------------- #
# Interface with Paganini
# ------------------------------------------------------- #


class _PaganiniEnv(NamedTuple):
    """Contextual information for interacting with paganini

    This stores the necessary information to extract the tuning result from paganini
    after having converted our grammar to their formalism.

    Args:
        variables: A mapping from (our) symbols to their corresponding paganini
            expression

        diagonals: A dictionary mapping paganini variables to their corresponding
            diagonals in paganini's internal representation. For instance, for the
            specification `T = z * MSet(T)`, paganini creates new variables v2, v3, v4,
            … representing T(z^2), T(z^3), T(z^4), … which it calls "diagonals". The
            dictionary below stores, for each symbol T and for each integer j, the
            paganini variable representing the j-th diagonal T(z^j) of T. This
            dictionary is empty when no Pólya operator is used in the specification.

        series_truncate: When Pólya operators are used, diagonals of degree larger or
            equal to `series_truncate` are approximated to zero.

    """

    variables: Dict[Symbol, pg.Expr]
    diagonals: Dict[pg.Variable, Dict[int, pg.Variable]]
    series_truncate: int

    def to_values(self) -> Dict[Symbol, List[float]]:
        """Convert paganini's output in the format expected by the generator.

        Examples:
            >>> from usainboltz import *
            >>> z, u, eps = Atom(), Marker("u"), Epsilon()
            >>> A, B =  RuleName("A"), RuleName("B")

            Some random algebraic specification.
            There is no Pólya operator so the ouput contains only arrays of size 2.

            >>> grammar = Grammar({A: z + B * A**2, B: z * u + eps})
            >>> values = OracleFromPaganini(grammar).tuning(A, singular=True)
            >>> print(len(values[z]))
            2
            >>> print(f"{values[z][1]:.8f}")
            0.20710678

            The specification of non-plane (Pólya) n-ary trees:

            >>> grammar = Grammar({A: z * MSet(A)})
            >>> values = OracleFromPaganini(grammar).tuning(A, singular=True)
            >>> print((len(values[z]), len(values[A])))
            (30, 30)
            >>> for j in range(1, 10):
            ...     print(f"{values[A][j]:.8f}")
                1.00000000
                0.13148788
                0.04035050
                0.01327774
                0.00445234
                0.00150187
                0.00050761
                0.00017168
                0.00005808
            >>> abs(values[z][1] ** 7 - values[z][7]) < 1e-9
            True
        """
        values: Dict[Symbol, List[float]] = dict()
        diags = self.diagonals if self.diagonals else None
        series_truncate = self.series_truncate if diags is not None else 2

        values[Epsilon()] = [1.0] * series_truncate

        for symbol, pg_expr in self.variables.items():
            # XXX. The atom seems to have a special treatment in paganini
            if symbol == Atom():
                values[symbol] = [pg_expr.value**j for j in range(series_truncate)]

            elif isinstance(pg_expr, pg.Variable):
                if diags is not None:
                    values[symbol] = [1.0]
                    diag = diags[pg_expr]
                    for j in range(1, series_truncate):
                        values[symbol].append(diag[j].value if j in diag else 0.0)
                else:
                    values[symbol] = [1.0, pg_expr.value]

            else:
                # Then pg_expr should be a constant.
                assert pg_expr.is_constant
                values[symbol] = [pg_expr.coeff] * series_truncate

        return values


def _to_paganini_constraint(
    lower_size: Optional[int], upper_size: Optional[int]
) -> Optional[pg.Constraint]:
    r"""Translates constraints over :py:class:`usainboltz.grammar.IteratedRule`
    into :py:class:`paganini.Constraint`"""
    if lower_size is not None and upper_size is not None:
        if lower_size == upper_size:
            return pg.eq(lower_size)
        else:
            raise ValueError("Paganini does not support mutliple constraints.")
    elif lower_size is not None:
        return pg.geq(lower_size)
    elif upper_size is not None:
        return pg.leq(upper_size)
    else:
        return None


def _to_paganini_rule(env: _PaganiniEnv, rule: Rule) -> pg.Expr:
    r"""Recursively translates :py:class:`usainboltz.grammar.Rule`
    into :py:class:`paganini.Expr` using the environnement `env` to
    set the expectations of pagagnini `Variables`
    """
    if isinstance(rule, Epsilon):
        return pg.Expr()
    elif isinstance(rule, Symbol):  # means Atom, Marker or RuleName
        return env.variables[rule]
    elif isinstance(rule, Union):
        return reduce(
            lambda x, y: x + y, map(partial(_to_paganini_rule, env), rule.args)
        )
    elif isinstance(rule, Product):
        return reduce(
            lambda x, y: x * y, map(partial(_to_paganini_rule, env), rule.args)
        )
    elif isinstance(rule, Seq):
        constraint = _to_paganini_constraint(rule.lower_size, rule.upper_size)
        return pg.Seq(_to_paganini_rule(env, rule.arg), constraint)
    elif isinstance(rule, Set):
        constraint = _to_paganini_constraint(rule.lower_size, rule.upper_size)
        return pg.Set(_to_paganini_rule(env, rule.arg), constraint)
    elif isinstance(rule, Cycle):
        constraint = _to_paganini_constraint(rule.lower_size, rule.upper_size)
        return pg.Cyc(_to_paganini_rule(env, rule.arg), constraint)
    elif isinstance(rule, MSet):
        constraint = _to_paganini_constraint(rule.lower_size, rule.upper_size)
        return pg.MSet(_to_paganini_rule(env, rule.arg), constraint)
    elif isinstance(rule, UCycle):
        constraint = _to_paganini_constraint(rule.lower_size, rule.upper_size)
        return pg.UCyc(_to_paganini_rule(env, rule.arg), constraint)
    else:
        raise TypeError("second argument should be of type usainboltz.grammar.Rule")


def _to_paganini_spec(
    grammar: Grammar, weights: Dict[Symbol, float]
) -> Tuple[_PaganiniEnv, pg.Specification]:
    r"""Convert a :py:class:`usainboltz.grammar.Grammar` with `weights`
    over symbols into a map :py:class:`usainboltz.grammar.Rule` ->
    :py:class:`paganini.Expr` and a :py:class:`paganini.Specification`

    Example:
        >>> from usainboltz import *
        >>> eps = Epsilon();  z = Atom(); B = RuleName()
        >>> grammar = Grammar({B: eps + z * B * B})

        >>> from usainboltz.oracle import _to_paganini_spec
        >>> env, spec = _to_paganini_spec(grammar, {z:1000})
        >>> env.variables[z], env.variables[B]
        (var1, var0)
        >>> spec
        var0 = 1  + var1^1 var0^2
    """

    spec = pg.Specification(series_truncate=30)
    env = _PaganiniEnv(
        variables=dict(),
        diagonals=spec._diag,  # XXX. Undocumented paganini feature.
        series_truncate=spec._series_truncate,  # XXX. Undocumented paganini feature.
    )

    for rulename in grammar.rules.keys():
        env.variables[rulename] = pg.Variable(weights.get(rulename))

    env.variables[Atom()] = pg.Variable(weights.get(Atom()))

    for m in grammar.markers():
        if m in weights:
            env.variables[m] = pg.Variable(weights[m])
        else:
            env.variables[m] = pg.Expr()

    for rulename, rule in grammar.rules.items():
        spec.add(env.variables[rulename], _to_paganini_rule(env, rule))

    return env, spec


class OracleFromPaganini(Oracle):
    r"""Build an oracle using
    `paganini <https://github.com/maciej-bendkowski/paganini>`_ : a package
    developped by M. Bendkowski and S. Dovgal

    .. todo:: add the reference to the paper
    """

    def __init__(self, grammar: Grammar):
        r"""Automatically build an oracle from a grammar using paganini.

        Args:
            grammar: the grammar for which to build the oracle.
        """
        super(OracleFromPaganini, self).__init__()
        self.grammar = grammar
        self.pg_method = pg.Method.FORCE

    def tuning(
        self, rule: RuleName, expectations=None, singular=False
    ) -> Dict[Symbol, List[float]]:
        r"""Run the oracle's algorithm

        Args:
          rule: the targeted symbol to tune w.r.t. ``expectations``

          expectations: a mapping between grammar markers and their targeted
              expectations after tuning

          singular: if ``True`` run the singular tuner (infinite expected size) else run
              a tuner targeting the given ``expectations``

        Returns:
            values: a mapping between grammar symbols and their weights in the Boltzmann
                model

        Note:
            If ``singular`` is ``True``, then ``expectations`` should
            be should be a dictionnary with grammar names (but the
            atom) as keys and ratios (between 0 and 1) as values.

           Else, ``expectations`` should be a dictionnary with keys as
            grammar names (but ``rule``) and the values should be
            integers.

        Examples:
           Use of the singular tuner for a binary tree grammar (size
           is the number of internal nodes):

           >>> from usainboltz import *
           >>> eps = Epsilon();  z = Atom(); B = RuleName()
           >>> grammar = Grammar({B: eps + z * B * B})
           >>> o = OracleFromPaganini(grammar)
           >>> values = o.tuning(B, singular=True)
           >>> abs(values[z][1]-0.25) < 1e-12
           True
           >>> abs(values[B][1]-2.) < 1e-12
           True

           As we expect ``z`` should be :math:`\frac14` (the
           singularity of :math:`\frac{1-\sqrt{1-4z}}{2}`)
        """

        if expectations is None:
            expectations = dict()

        if rule in expectations:
            raise ValueError("You must not set any constraint over {}".format(rule))

        # Check the values of expectations w.r.t. singular or not
        if singular:
            if any(x < 0 or x > 1 for x in expectations.values()):
                raise ValueError("Ratios must be between 0 and 1")
        elif all(x < 1 for x in expectations.values()):
            raise ValueError("The expected numbers must be greater than 1")

        env, spec = _to_paganini_spec(self.grammar, expectations)

        env.variables[rule].set_expectation(None)
        for k, v in expectations.items():
            env.variables[k].set_expectation(v)

        try:
            if singular:
                spec.run_singular_tuner(env.variables[Atom()], method=self.pg_method)
            else:
                spec.run_tuner(env.variables[rule], method=self.pg_method)
        except SolverError:
            raise ValueError("Your expected sizes can not be targeted")

        return env.to_values()

    def __repr__(self):
        return "OracleFromPaganini({})".format(self.grammar)


# ------------------------------------------------------- #
# Convertion of a python dictionnary into an oracle
# ------------------------------------------------------- #


class OracleFromDict(Oracle):
    dict_: Dict[Symbol, List[float]]

    def __init__(self, d: TypeUnion[Dict[Symbol, List[float]], Dict[Symbol, float]]):
        super(OracleFromDict, self).__init__()
        if not (isinstance(d, dict)):
            raise TypeError("The argument should be a dictionnary")

        # Take one arbitrary value of the dictionary
        for v in d.values():
            if isinstance(v, (float, int)):
                self.dict_ = {
                    key: [1.0, value] for key, value in d.items()  # type: ignore
                }
            else:
                # mypy is not clever enough to see that this is well-typed (is it?).
                self.dict_ = d  # type: ignore
            return
        raise ValueError("OracleFromDict received an empty dictionary")

    def tuning(self, *args, **kwargs) -> Dict[Symbol, List[float]]:
        return self.dict_

    def __repr__(self):
        return "OracleFromDict({})".format(self.dict_)


# ------------------------------------------------------- #
# Interface with combstruct (maple)
# ------------------------------------------------------- #


def _to_combstruct_constraint(
    lower_size: Optional[int], upper_size: Optional[int]
) -> str:
    r"""Translates sizes constraint over
    :py:class:`usainboltz.grammar.IteratedRule` into `combstruct`
    constraints.

    Examples:
        >>> from usainboltz import * # doctest: +SKIP
        >>> z = Atom(); S = RuleName("S") # doctest: +SKIP
        >>> o = OracleFromNewtonGF(Grammar({S: Seq(z, leq=3)})) # doctest: +SKIP
        >>> o.combstruct_spec # doctest: +SKIP
        '{S = Seq(Atom, card <= 3)}'
        >>> o = OracleFromNewtonGF(Grammar({S: Seq(z, geq=3)})) # doctest: +SKIP
        >>> o.combstruct_spec # doctest: +SKIP
        '{S = Seq(Atom, 3 <= card)}'
        >>> o = OracleFromNewtonGF(Grammar({S: Seq(z, eq=3)})) # doctest: +SKIP
        >>> o.combstruct_spec # doctest: +SKIP
        '{S = Seq(Atom, card = 3)}'
    """

    x = (lower_size, upper_size)
    if x == (None, None):
        return ""
    elif x == (lower_size, None):
        return f", {lower_size} <= card"
    elif x == (None, upper_size):
        return f", card <= {upper_size}"
    else:
        if lower_size == upper_size:
            return f", card = {upper_size}"
        else:
            print(
                "WARNING: NewtonGF may not handle constraints "
                + "over lower and upper sizes",
                file=sys.stderr,
            )
            return f", card <= {upper_size}, {lower_size} <= card"


def _to_combstruct_rule(rule: Rule) -> str:
    r"""Recursively translates :py:class:`~usainboltz.grammar.Rule`
    into `combstruct[specification]`
    """

    if isinstance(rule, Epsilon):
        return "Epsilon"
    elif isinstance(rule, Atom):
        return "Atom"
    elif isinstance(rule, Marker):
        return "Epsilon"
    elif isinstance(rule, RuleName):
        return str(rule)
    elif isinstance(rule, Union):
        return "Union(" + ",".join(map(_to_combstruct_rule, rule.args)) + ")"
    elif isinstance(rule, Product):
        return "Prod(" + ",".join(map(_to_combstruct_rule, rule.args)) + ")"
    elif isinstance(rule, Seq):
        constraint = _to_combstruct_constraint(rule.lower_size, rule.upper_size)
        return f"Sequence({_to_combstruct_rule(rule.arg)}{constraint})"
    elif isinstance(rule, Set):
        constraint = _to_combstruct_constraint(rule.lower_size, rule.upper_size)
        return f"Set({_to_combstruct_rule(rule.arg)}{constraint})"
    elif isinstance(rule, Cycle):
        constraint = _to_combstruct_constraint(rule.lower_size, rule.upper_size)
        return f"Cycle({_to_combstruct_rule(rule.arg)}{constraint})"
    elif isinstance(rule, MSet):
        constraint = _to_combstruct_constraint(rule.lower_size, rule.upper_size)
        return f"Set({_to_combstruct_rule(rule.arg)}{constraint})"
    elif isinstance(rule, UCycle):
        constraint = _to_combstruct_constraint(rule.lower_size, rule.upper_size)
        return f"Cycle({_to_combstruct_rule(rule.arg)}{constraint})"
    #  elif isinstance(rule, PSet):
    #  raise NotImplementedError
    else:
        raise TypeError("first argument should be of type usainboltz.grammar.Rule")


def _to_combstruct_spec(grammar: Grammar) -> str:
    spec = set()

    for marker in grammar.markers():
        spec.add(f"{marker}=Epsilon")

    for rulename, rule in grammar.rules.items():
        spec.add(f"{rulename} = {_to_combstruct_rule(rule)}")

    return "{" + ",".join(spec) + "}"


newtongf_installed: bool = False

try:
    from sage.interfaces.maple import maple

    maple.load("combstruct")
    maple.load("NewtonGF")
    newtongf_installed = True
    __all__.append("OracleFromNewtonGF")
except ImportError:
    pass
except RuntimeError:
    pass


class OracleFromNewtonGF(Oracle):
    r"""Build an orcale using `NewtonGF
    <http://perso.ens-lyon.fr/bruno.salvy/software/the-newtongf-package/>`_

    Note:
        If you want to use OracleFormNewtonGF, please install the
        NewtonGF library for Maple into you Maple lib/ directory,
        or precise a lib/ directory to Maple i.e.
        maple('libname:=\"NewtonGF_path\",libname:')
    """

    def __init__(self, grammar: Grammar):
        r"""Build an oracle from a grammar"""

        if not newtongf_installed:
            raise ImportError(
                "You cannot use OracleFromNewtonGF because your "
                + "Sagemath, Maple or NewtonGF installation is not "
                + "consistent."
            )

        self.grammar = grammar
        self.combstruct_spec = _to_combstruct_spec(grammar)

    def tuning(
        self, rule: Symbol, expectations=None, singular=False
    ) -> Dict[Symbol, List[float]]:
        r"""Run the oracle's algorithm

        Args:
            rule: the targeted symbol to tune w.r.t. ``expectations``

            expectations: a mapping between grammar symbols and their targeted
                expectations after tuning

          singular: if ``True`` run the singular tuner (infinite expected size) else run
            a tuner targeting the given ``expectations``

        Returns:
            values: a mapping between grammar symbols and their weights in the Boltzmann
                model

        Note:
            In the case of NewtonGF, only **univariate**
            specifications are supported, so:
            * if `expectations` is provided it must have a key corresponding
            to :py:class:`~usainboltz.grammar.Atom()`,
            * the markers (see :py:class:`~usainboltz.grammar.Marker`)
            will not be handled.

        Examples:
           Use of the singular tuner for a binary tree grammar (size
           is the number of internal nodes):

           >>> from usainboltz import *
           >>> eps = Epsilon();  z = Atom(); B = RuleName()
           >>> grammar = Grammar({B: eps + z * B * B})
           >>> o = OracleFromNewtonGF(grammar) # doctest: +SKIP
           >>> values = o.tuning(B,singular=True) # doctest: +SKIP
           >>> values[z] # doctest: +SKIP
           0.25
           >>> values[B] # doctest: +SKIP
           1.999999988

           As we expect ``z`` should be :math:`\frac14` (the
           singularity of :math:`\frac{1-\sqrt{1-4z}}{2}`)

        """

        # To remove if we do the choice to autorize only one atom per grammar
        if len(self.grammar.markers()) > 0:
            print(
                "NewtonGF deals only with univariate specifications "
                + "and there are several markers in your one",
                file=sys.stderr,
            )

        labeled = "labeled" if self.grammar.labelled else "unlabeled"

        if not singular and (expectations is None or Atom() not in expectations):
            raise ValueError(
                "You must set an expectations over the size of the structure"
            )

        rho = 0
        if singular:
            rho = maple(f"Radius({self.combstruct_spec}, {labeled})")
        else:
            rho = maple(
                f"BoltzmannParameter({self.combstruct_spec}, {labeled}, {rule}, "
                + f"{expectations[Atom()]})"
            )

        oracle = maple(
            f"NumericalNewtonIteration({self.combstruct_spec}, {labeled})({rho})"
        )
        table = str.maketrans({"=": ":", "[": "{", "]": "}"})

        self.grammar_symbols = {
            str(symbol): symbol
            for symbol in self.grammar.markers() | set(self.grammar.rules)
        }

        values = eval(str(oracle).translate(table), globals(), self.grammar_symbols)
        values[Atom()] = float(rho)

        values_list = {symbol: [1.0, value] for symbol, value in values.items()}

        return values_list

    def __repr__(self):
        return "OracleFromNewtonGF({})".format(self.grammar)

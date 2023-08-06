# coding: utf-8

# Copyright 2019-2022 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

import warnings

from usainboltz.generator import Generator, union_builder
from usainboltz.grammar import (
    Atom,
    Cycle,
    Epsilon,
    Grammar,
    Marker,
    MSet,
    Product,
    RuleName,
    Seq,
    Set,
    UCycle,
    Union,
)
from usainboltz.oracle import OracleFromDict, OracleFromPaganini, build_oracle

__all__ = [
    "Generator",
    "union_builder",
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
    "build_oracle",
    "OracleFromPaganini",
    "OracleFromDict",
]


# XXX: remove me
# XXX: https://github.com/maciej-bendkowski/paganini/issues/6
warnings.filterwarnings("ignore", category=UserWarning, module="cvxpy.problems.problem")


try:
    from usainboltz.oracle import OracleFromNewtonGF  # noqa: F401

    __all__.append("OracleFromNewtonGF")
except ImportError:
    pass

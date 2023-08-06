# Copyright 2019-2022 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

"""RNA secondary structures"""

from typing import List, TextIO, Tuple, Union as TypeUnion

from usainboltz import (
    Atom,
    Epsilon,
    Generator,
    Grammar,
    Marker,
    RuleName,
    union_builder,
)
from usainboltz.generator import rng_seed

B, S, z = RuleName("B"), RuleName("S"), Atom()
A, U, C, G = Marker("A"), Marker("U"), Marker("C"), Marker("G")


grammar = Grammar(
    {S: B * z * (S + Epsilon()) + B * z * S * z * (S + Epsilon()), B: A + U + C + G}
)
generator = Generator(grammar, S)


dual = {A: U, U: A, C: G, G: C}


def identity(x):
    return x


# ---
# RNA secondary structures as sequences of bases with offsets
# ---


# The Python type of sequences of bases.
SEQ = List[TypeUnion[str, Tuple[str, int]]]

# Tagged union of a SEQ or an Epsilon
SEQ_E = Tuple[int, TypeUnion[SEQ, str]]


def build_seq_empty(_: str) -> SEQ:
    return []


build_seq_s_or_e = union_builder(identity, build_seq_empty)


def build_seq_prefix(t: Tuple[str, SEQ_E]) -> SEQ:
    base, z, se = t
    return [base] + build_seq_s_or_e(se)


def build_seq_matching(t: Tuple[str, SEQ, str, SEQ_E]) -> SEQ:
    base, z, s, z, se = t
    offset = len(s) + 1
    return [(base, offset)] + s + [dual[base]] + build_seq_s_or_e(se)


build_seq_S = union_builder(build_seq_prefix, build_seq_matching)


# ---
# RNA secondary structures as forests
# ---


class Counter:
    def __init__(self):
        self.n = 0

    def next(self) -> int:
        r = self.n
        self.n += 1
        return r


# the type of forests
FOREST = List["Tree"]


def forest_str(f: FOREST) -> str:
    return "[{}]".format(", ".join(map(str, f)))


def forest_dot(f: FOREST, counter: Counter, file: TextIO) -> List[int]:
    return [tree.dot(counter, file) for tree in f]


class Tree:
    def __init__(self, children: FOREST):
        self.children = children

    def dot(self, counter, file) -> int:
        my_id = counter.next()
        children_ids = forest_dot(self.children, counter, file)
        file.write(f'  {my_id} ["shape"="point"]\n')
        for child_id in children_ids:
            file.write(f"  {my_id} -> {child_id}\n")
        return my_id

    def __str__(self):
        return f"Tree({forest_str(self.children)})"


def build_forest_prefix(t: Tuple[str, str, FOREST]) -> FOREST:
    _, _, s = t
    return s


def build_forest_matching(t: Tuple[str, str, FOREST, str, FOREST]) -> FOREST:
    _, _, s, _, sp = t
    return [Tree(s)] + sp


def build_forest_empty(_) -> FOREST:
    return []


build_forest_S = union_builder(build_forest_prefix, build_forest_matching)
build_forest_Sp = union_builder(identity, build_forest_empty)


# ---
# The order to RNA secondary structures
# ---


def order_prefix(t):
    _, _, s = t
    return s


def order_matching(t):
    _, _, s, _, sp = t
    order_s, _ = s
    order_sp, flag_sp = sp
    if order_s < order_sp:
        return sp
    if order_s > order_sp:
        return (order_s, True)
    if flag_sp:
        return (order_sp + 1, False)
    else:
        return (order_sp, True)


def order_empty(_):
    return (1, False)


order_S = union_builder(order_prefix, order_matching)
order_Sp = union_builder(identity, order_empty)


if __name__ == "__main__":
    SEED = 0x8FFF2FAD00DC576B
    SIZE = 15

    print(f"=> Using seed: 0x{SEED:x}")

    print("=> Grammar:")
    print(grammar)

    print("=> Using the default builders:")
    rng_seed(SEED)
    res = generator.sample((SIZE, SIZE))
    print(res.obj)

    print("=> A large RNA secondary structure:")
    rng_seed(SEED)
    res = generator.sample((10000, 15000))
    print(res.sizes)

    print("=> Using expectations:")
    rng_seed(SEED)
    generator2 = Generator(grammar, expectations={A: 3000, z: 10000})
    res = generator.sample({z: (10000, 15000), A: (2800, 15000)})
    print(res.sizes)

    print("=> Using the sequence builders:")
    rng_seed(SEED)
    generator.set_builder(S, build_seq_S)
    res = generator.sample((SIZE, SIZE))
    print(res.obj)

    exit(0)

    print("=> Using the forest builders:")
    generator.set_builder(S, build_forest_S)
    rng_seed(SEED)
    res = generator.sample((SIZE, SIZE))
    print(forest_str(res.obj))
    with open("forest.dot", "w") as file:
        file.write("digraph G {\n")
        forest_dot(res.obj, Counter(), file)
        file.write("}\n")

    print("=> Using the order builders:")
    generator.set_builder(S, order_S)
    rng_seed(SEED)
    res = generator.sample((SIZE, SIZE))
    print(res.obj)

# Usain Boltz

Usain Boltz is a Python/Cython library meant to automate the random generation
of tree-like structures.

The library was primarily designed to be used with the
[Sagemath](https://sagemath.org) mathematics software system but Sagemath is no
longer a dependency and the library is now perfectly usable both within and
without a Sagemath environment.

## Install

### Via pip (recommended)

Usain Boltz is available on PyPI, just type:

```
pip3 install usainboltz
```

### From source

System requirements:

- One of our dependencies requires `cmake` to build. It is installed by default
  on most distributions but if you encounter build errors with `osqp` that may
  be the reason.

- You also need to have [`cython`](https://cython.org/) installed on your
  system to be able to build Usain Boltz.


Build, test and install:

- Run `make build` to build the `C` and `Cython` extensions
- Run `make test` to run the doctests
- Run `python3 setup.py install [--user]` to install in your current python
  environment

### Sagemath

Both installation methods make Usain Boltz available to Sagemath

## Documentation

Provided you have [`sphinx`](https://www.sphinx-doc.org) installed, you can
build the documentation with `make doc`.

### Examples and demo

Some examples are available in the `examples` and `sage_examples` modules in
the documentation. In particular, the `sage_examples` module illustrates how
Usain Boltz can be used to generate sage objects.

A sage notebook is available in the `demo/` folder which shows how Usain Boltz
can be used to generate various objects related to binary trees from the same
grammar and generator.

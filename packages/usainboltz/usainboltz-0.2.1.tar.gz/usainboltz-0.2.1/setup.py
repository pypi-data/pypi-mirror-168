# coding: utf8

from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

with open("README.md", "r") as file:
    long_description = file.read()

extra_compile_args = ["-std=c++11", "-Wpedantic", "-Wextra"]

extensions = [
    Extension(
        "usainboltz.cpp_simulator",
        sources=["src/usainboltz/cpp_simulator.cpp", "src/xoshiro/cpp_xoshiro.cpp"],
        include_dirs=["src/xoshiro", "src/usainboltz"],
        language="c++",
        extra_compile_args=extra_compile_args,
    ),
    Extension(
        "usainboltz.simulator",
        sources=["src/usainboltz/simulator.pyx"],
        include_dirs=["src/xoshiro", "src/usainboltz"],
        language="c++",
        extra_compile_args=extra_compile_args,
    ),
    Extension(
        "usainboltz.generator",
        sources=["src/usainboltz/generator.pyx"],
        include_dirs=["src/xoshiro/", "src/usainboltz"],
        language="c++",
        extra_compile_args=extra_compile_args,
    ),
]

setup(
    name="usainboltz",
    version="0.2.1",
    author="Matthieu Dien, Martin Pépin",
    author_email="kerl@wkerl.me",
    description="Fast Boltzmann random generators for SageMath",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ParComb/usain-boltz",
    project_urls={
        "Bug Tracker": "https://gitlab.com/ParComb/usain-boltz/issues",
        "Documentation": "https://usain-boltz.readthedocs.io",
        "Source Code": "https://gitlab.com/ParComb/usain-boltz",
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
    ext_modules=cythonize(extensions, language_level=3),
    install_requires=["paganini >= 1.3.3", "cvxpy >= 1.2.0"],
    license="GPLv3+",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Cython",
        "Programming Language :: C++",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

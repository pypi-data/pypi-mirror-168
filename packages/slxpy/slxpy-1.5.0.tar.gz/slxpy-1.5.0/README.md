# Slxpy
![PyPI](https://img.shields.io/pypi/v/slxpy)
[![MATLAB FileExchange](https://img.shields.io/badge/MATLAB-FileExchange-blue.svg)](https://www.mathworks.com/matlabcentral/fileexchange/100416-slxpy)

Toolchain for seamlessly generating efficient Simulink-to-Python binding and gym-like environment wrapper.

> For smooth integration, it's recommended to read through the [wiki](https://github.com/jjyyxx/slxpy/wiki) carefully

## Features

- Almost complete Simulink and Embedded Coder features support
- Compatible with a wide range of MATLAB versions
- Help tuning Simulink code generation config
- Mininal dependencies and cross-platform, not depending on MATLAB after Simulink code generation step
- Exchange array data with numpy for efficiency
- Raw and gym environment wrapper, with seeding and parameter randomization support
- Automatic single-node parallelization with vector environment
- Generate human-readable object `__repr__` for ease of use
- Automatically generate stub file to assist development (with pybind11-stubgen)
- Compile with all modern C++ compilers

## Prerequisities & Installation & Quick start

You need to prepare Python, optionally MATLAB and a C++ compiler to begin with slxpy. See the [wiki](https://github.com/jjyyxx/slxpy/wiki) for details.

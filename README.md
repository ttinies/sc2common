[![Anaconda-Server Badge](https://anaconda.org/versentiedge/sc2common/badges/version.svg)](https://anaconda.org/versentiedge/sc2common)
[![PyPI](https://img.shields.io/pypi/v/sc2common.svg)](https://pypi.org/project/sc2common/)
[![Build Status](https://travis-ci.org/ttinies/sc2common.svg?branch=master)](https://travis-ci.org/ttinies/sc2common)
[![Coverage Status](https://coveralls.io/repos/github/ttinies/sc2common/badge.svg?branch=master)](https://coveralls.io/github/ttinies/sc2common?branch=master)
![Crates.io](https://img.shields.io/crates/l/rustc-serialize.svg)

# common values, functions and objects for any packages that support SC2

#### Purpose

This package definse constants, types, containers and functions commonly used throughout the Starcraft 2 deveopment
space.  Consolidating these into a single package allows developers to utilize these items while ensuring they are
centrally defined and implemented once. Its usage is as a library only with no specific functionality to invoke except
through one's own code.

#### Installation

This package is often automatically installed as a dependency by other packages that support Starcraft 2 in some way.
Nevertheless, this package can also be directly installed by itself.

It is recommended to install this pacakge using [Anaconda](https://anaconda.org/versentiedge/sc2common).  However, installation is also supported via [pypi.org](https://pypi.org/project/sc2common/).
> EXAMPLE: `conda install -c versentiedge sc2common`

> EXAMPLE: `pip install sc2common`

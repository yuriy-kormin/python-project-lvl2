## Tests & statuses:
[![Actions Status](https://github.com/yuriy-kormin/python-project-lvl2/workflows/hexlet-check/badge.svg)](https://github.com/yuriy-kormin/python-project-lvl2/actions)
[![test](https://github.com/yuriy-kormin/python-project-lvl2/actions/workflows/tests.yml/badge.svg)](https://github.com/yuriy-kormin/python-project-lvl2/actions/workflows/tests.yml)
<a href="https://codeclimate.com/github/yuriy-kormin/python-project-lvl2/test_coverage"><img src="https://api.codeclimate.com/v1/badges/7f241587067d2985f1dc/test_coverage" /></a>
[![linter-run](https://github.com/yuriy-kormin/python-project-lvl2/actions/workflows/linter-run.yml/badge.svg)](https://github.com/yuriy-kormin/python-project-lvl2/actions/workflows/linter-run.yml)
<a href="https://codeclimate.com/github/yuriy-kormin/python-project-lvl2/maintainability"><img src="https://api.codeclimate.com/v1/badges/7f241587067d2985f1dc/maintainability" /></a>

## Stack
![Python](https://img.shields.io/badge/python-blue?style=plastic)
![pytest](https://img.shields.io/badge/pytest-success?style=plastic)
![poetry](https://img.shields.io/badge/poetry-blueviolet?style=plastic)
![poetry](https://img.shields.io/badge/argparse-lightgrey?style=plastic)



It's a simple CLI utility to find difference between 2 files. It also supports nested data structures.

Analizing files formats:  
  - .json 
  - .yml 

 Outputs variants: 
  - plain
  - stylish
  - json

#### Utility processing includes three steps:
  - Reading input files
  - Comparing data and find differences
  - Based on differences, building working result in selected format (default is stylish) 

The working process is based on a single internal representation format, which will be the same regardless of the format of the input files.  
Thanks to this approach, it is possible to add additional reading formats without significantly modifying the code.  
The same way is used to display the result.

## Prepare for installation
These tools must be configured on your system:
 - [git](https://github.com/git-guides/install-git)
 - [python](https://www.python.org/)
 - [poetry](https://python-poetry.org/docs/)
 - [pip](https://pip.pypa.io/en/stable/)

## Installation
At first point, poetry will download and install all the necessary packages to build the utility

    git clone https://github.com/yuriy-kormin/python-project-lvl2.git
    cd python-project-lvl2
    make install

The second step is to build and install the package

    make build
    pip install dist/hexlet_code-0.1.0-py3-none-any.whl

[![asciicast](https://asciinema.org/a/508199.svg)](https://asciinema.org/a/508199)

## Examples of using
#### Search diff with flat files in .json format
[![asciicast](https://asciinema.org/a/508190.svg)](https://asciinema.org/a/508190)
#### Search diff with flat files in .yml format
[![asciicast](https://asciinema.org/a/508194.svg)](https://asciinema.org/a/508194)
#### Search diff with nested files
[![asciicast](https://asciinema.org/a/508202.svg)](https://asciinema.org/a/508202)

## Build result in different output format

#### Plain output example
[![asciicast](https://asciinema.org/a/508203.svg)](https://asciinema.org/a/508203)
#### JSON output example
[![asciicast](https://asciinema.org/a/508205.svg)](https://asciinema.org/a/508205)

#!/bin/bash
set -e
# cd to self bash script directory
cd $( dirname ${BASH_SOURCE[0]})
echo Running flake8
flake8 pyflutterinstall tests test_install
echo Running pylint
pylint pyflutterinstall tests test_install
echo Running mypy
mypy pyflutterinstall tests test_install
echo Linting complete!
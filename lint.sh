#!/bin/bash
set -e
# cd to self bash script directory
cd "${BASH_SOURCE[0]%/*}"

echo Fixing code style with black
black pyflutterinstall tests test_install

echo Running flake8
flake8 pyflutterinstall tests test_install
echo Running pylint
pylint pyflutterinstall tests test_install
echo Running mypy
mypy pyflutterinstall tests test_install
echo Linting complete!
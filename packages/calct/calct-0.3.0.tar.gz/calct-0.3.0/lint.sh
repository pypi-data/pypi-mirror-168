#!/usr/bin/env bash

python -m black --check calct tests
python -m isort --check-only calct tests
python -m mypy -p calct -p tests
python -m flake8 calct tests
python -m pylint calct tests

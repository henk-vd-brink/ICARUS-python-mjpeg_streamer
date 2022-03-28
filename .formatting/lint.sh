#!/bin/sh -e
set -x

mypy src
black src --check
black tests --check
isort --check-only src
isort --check-only tests
flake8
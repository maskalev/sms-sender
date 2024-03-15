#!/bin/bash

pip install -r requirements-codequality.txt
isort --profile black --line-length 79 . --check --diff
black --line-length 79 . --check --diff

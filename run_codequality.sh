#!/bin/bash

pip install isort black
isort --profile black --line-length 79 . --check --diff
black --line-length 79 . --check --diff

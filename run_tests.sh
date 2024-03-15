#!/bin/bash

pip install -r requirements-tests.txt
coverage run -m pytest
coverage report

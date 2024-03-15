#!/bin/bash

pip install -r requirements.txt
coverage run -m pytest
coverage report

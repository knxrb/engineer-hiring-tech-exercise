#!/bin/bash

# It may be necessary to give permissions to execute this script: chmod +x tools/dev/coverage.sh

coverage run --branch -m pytest tests/test_*.py
coverage report -m --fail-under=100 --omit=tests/*,.venv/*
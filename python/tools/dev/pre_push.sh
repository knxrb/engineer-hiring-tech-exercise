#!/bin/bash

# It may be necessary to give permissions to execute this script: chmod +x tools/dev/pre_push.sh

# Text Colours
purple      () { printf "\e[35m" ; "$@" ; printf "\e[0m"; }
lt_yellow   () { printf "\e[33m" ; "$@" ; printf "\e[0m"; }
green       () { printf "\e[32m" ; "$@" ; printf "\e[0m"; }

# Dependency and Security Checks
lt_yellow echo 'Checking dependencies status.' && \
uv lock --check

echo && lt_yellow echo 'Bandit is checking for security issues.' && \
bandit -r -q . -x ./.venv --format screen

echo && purple echo 'Checking for errors, potential problems, convention violations and complexity (Ruff).' && \
uvx ruff check . && echo

# Tests, Coverage, and Formatting Checks
echo && purple echo 'Running unit tests and checking coverage:' && \
tools/dev/coverage.sh

echo && green echo 'Pre-push script complete.'

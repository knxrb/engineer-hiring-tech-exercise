#!/bin/bash

# It may be necessary to give permissions to execute this script: chmod +x tools/dev/coverage.sh

coverage run
coverage report -m

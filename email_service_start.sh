#!/usr/bin/env bash

# This can be run from within a crontab as needed.

# activate the virtual environment
source ../venv/bin/activate     # back by 1 DIR only _> place venv only 1 dir back from the project folder

python3 email_script.py
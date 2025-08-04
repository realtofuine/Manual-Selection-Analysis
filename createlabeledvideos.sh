#!/bin/bash

# Load Anaconda first (BEFORE trying to activate env)
# module load anaconda  # or whichever is available and has your env

# Initialize shell support for conda (needed for conda activate)

eval "$(conda shell.bash hook)"
# Now activate your env
conda activate manualenv
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd $SCRIPT_DIR
python createlabeledvideos.py
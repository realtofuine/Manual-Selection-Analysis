#!/bin/bash

# Load Anaconda first (BEFORE trying to activate env)
# module load anaconda  # or whichever is available and has your env

eval "$(conda shell.bash hook)"
# Now activate your env
conda activate manualenv

python deeplabcutanalyze.py --path "$1"
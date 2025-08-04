#!/bin/bash

eval "$(conda shell.bash hook)"
# Now activate your env
conda activate manualenv

# echo "Python path: $(which python)"
# echo "Active conda env: $CONDA_DEFAULT_ENV"
# echo "Running script with video: $1 and ROI: $2"

python generateVideos.py --video "$1" --roi "$2" --output "$3"

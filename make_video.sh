#!/bin/bash

eval "$(conda shell.bash hook)"
# Now activate your env
conda activate manualenv
cd $1

# ffmpeg -threads 4 -framerate 30 -pattern_type glob -i "IMG_*.JPG" -vf format=yuv420p -c:v libx264 -preset ultrafast -movflags +faststart $2
ffmpeg -threads 4 -framerate 30 -pattern_type glob -i "IMG_*.JPG" -vf format=yuv420p -c:v libx264 -preset ultrafast -crf 18 -movflags +faststart $2
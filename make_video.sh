#!/bin/bash
#SBATCH -J ffmpeg_video
#SBATCH -o /output/makevideo_output-%j.log
#SBATCH -n 4
#SBATCH -p batch
#SBATCH --mem 16G
#SBATCH -t 1:00:00

module load ffmpeg
cd $1

# ffmpeg -threads 4 -framerate 30 -pattern_type glob -i "IMG_*.JPG" -vf format=yuv420p -c:v libx264 -preset ultrafast -movflags +faststart $2
ffmpeg -threads 4 -framerate 30 -pattern_type glob -i "IMG_*.JPG" -vf format=yuv420p -c:v libx264 -preset ultrafast -crf 18 -movflags +faststart $2
#!/bin/bash
#SBATCH -n 64
#SBATCH -p batch
#SBATCH --mem=16G
#SBATCH -J generateVids
#SBATCH -o output/generateVids-%j.out
#SBATCH -t 2:00:00


# Load Anaconda first (BEFORE trying to activate env)
module load anaconda  # or whichever is available and has your env

# Initialize shell support for conda (needed for conda activate)
source /gpfs/runtime/opt/anaconda/2020.02/bin/activate

# Now activate your env
conda activate manualenv

# Load ffmpeg if needed after environment
module load ffmpeg

# echo "Python path: $(which python)"
# echo "Active conda env: $CONDA_DEFAULT_ENV"
# echo "Running script with video: $1 and ROI: $2"

python generateVideos.py --video "$1" --roi "$2" --output "$3"

#!/bin/bash

#SBATCH -N 1
#SBATCH -p gpu --gres=gpu:1
#SBATCH --mem 32G
#SBATCH -J deeplabcutanalyze
#SBATCH -o output/deeplabcutanalyze-%j.out
#SBATCH -t 2:00:00

# Load Anaconda first (BEFORE trying to activate env)
# module load anaconda  # or whichever is available and has your env

# Initialize shell support for conda (needed for conda activate)
source /gpfs/runtime/opt/anaconda/2020.02/bin/activate

# Now activate your env
conda activate DEEPLABCUT
python deeplabcutanalyze.py --path "$1"
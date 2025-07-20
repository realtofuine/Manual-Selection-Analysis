#!/bin/bash

#SBATCH -n 64
#SBATCH -p batch
#SBATCH --mem 16G
#SBATCH -J analyzeData
#SBATCH -o /users/rrai8/zebrafish_analysis/Manual-Selection/output/analyzeData-%j.out
#SBATCH -t 2:00:00

# Load Anaconda first (BEFORE trying to activate env)
# module load anaconda  # or whichever is available and has your env

# Initialize shell support for conda (needed for conda activate)
cd "$(dirname "$(realpath "$0")")"
source /gpfs/runtime/opt/anaconda/2020.02/bin/activate
conda activate manualenv
python analyzeData.py --path "$1"
print("Data analysis completed successfully.")
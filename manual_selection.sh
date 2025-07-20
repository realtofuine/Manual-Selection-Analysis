#!/bin/bash

#EDIT THESE 2 PARAMETERS
roi_zip="/users/rrai8/zebrafish_analysis/Manual-Selection/rois/roi-7-16.zip"
image_folder="/users/rrai8/2025_07_16"


dir="$HOME/scratch/$(basename "$image_folder")"
video_path="$HOME/scratch/videos/$(basename "$image_folder")"
video=${video_path}.mp4
mkdir ${dir}
mkdir -p video_path

module load anaconda
source /gpfs/runtime/opt/anaconda/2020.02/bin/activate
#Create environments if they don't exist
if conda info --envs | grep -qE "^DEEPLABCUT[[:space:]]"; then
    echo "✅ DEEPLABCUT environment exists"
else
    echo "🚀 Creating environment"
    conda env create -n "DEEPLABCUT" -f DEEPLABCUT.yaml
fi

if conda info --envs | grep -qE "^manualenv[[:space:]]"; then
    echo "✅ manualenv environment exists"
else
    echo "🚀 Creating environment"
    conda env create -n "manualenv" -f manualenv.yml
fi

#Submit make combined video job
jid0=$(sbatch make_video.sh $image_folder $video | awk '{print $4}')
echo "Submitted make_video job: $jid0"

# Submit CPU job
jid1=$(sbatch --dependency=afterok:$jid0 generateVids.sh $video $roi_zip $dir | awk '{print $4}')
echo "Submitted generateVids job: $jid1"

# Submit GPU job to run after CPU job finishes
jid2=$(sbatch --dependency=afterok:$jid1 deeplabcutanalyze.sh $dir | awk '{print $4}')
echo "Submitted deeplabcutanalyze job: $jid2"

# Submit postprocess job to run after GPU job finishes
jid3=$(sbatch --dependency=afterok:$jid2 analyzeData.sh $dir | awk '{print $4}')
echo "Submitted data analysis job: $jid3"
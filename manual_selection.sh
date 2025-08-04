#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#EDIT THESE 2 PARAMETERS
roi_zip="$SCRIPT_DIR/rois/roi-sample.zip"
image_folder="$SCRIPT_DIR/images/sample"


dir="$SCRIPT_DIR/output/$(basename "$image_folder")"
video_path="$SCRIPT_DIR/videos/$(basename "$image_folder")"
video=${video_path}.mp4
mkdir ${dir}


cd $SCRIPT_DIR
#Create environments if they don't exist
# if conda info --envs | grep -qE "^DEEPLABCUT[[:space:]]"; then
#     echo "✅ DEEPLABCUT environment exists"
# else
#     echo "🚀 Creating environment. Make sure conda is installed!"
#     conda env create -n "DEEPLABCUT" -f DEEPLABCUT.yaml
# fi
eval "$(conda shell.bash hook)"

if conda info --envs | grep -qE "^manualenv[[:space:]]"; then
    echo "✅ manualenv environment exists"
else
    echo "🚀 Creating environment"
    conda env create -n "manualenv" -f manualenv.yml
fi

set -euo pipefail

#Submit make combined video job
bash make_video.sh $image_folder $video
echo "Completed make_video job"

# Submit CPU job
bash generateVids.sh $video $roi_zip $dir
echo "Submitted generateVids job"

# Submit GPU job to run after CPU job finishes
bash deeplabcutanalyze.sh $dir
echo "Submitted deeplabcutanalyze job"

# Submit postprocess job to run after GPU job finishes
bash analyzeData.sh $dir 
echo "Submitted data analysis job"
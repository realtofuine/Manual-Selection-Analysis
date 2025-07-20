import os
import re
import subprocess
import deeplabcut
import cv2
from read_roi import read_roi_zip

# Set the full path to your config.yaml
config_path = '/users/rrai8/zebrafish_analysis/Manual-Selection/singlelarvae_imaging-rishi-2025-06-13/config-oscar.yaml'

# Path to the folder containing the cropped videos
video_folder = '/users/rrai8/scratch/2025_07_12'

# Collect all .mp4 files
video_files = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.endswith('.mp4')]

# Iterate and create labeled videos
for video in video_files:
    print(f"Processing: {video}")
    deeplabcut.create_labeled_video(config_path, [video], filtered=False, pcutoff=0)
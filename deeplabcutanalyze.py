import argparse
import http.client
import json

import deeplabcut

parser = argparse.ArgumentParser(description="Analyze deeplabcut videos.")
parser.add_argument("--path", type=str, required=True, help="Path to the input video file.")
args = parser.parse_args()
deeplabcut.analyze_videos("singlelarvae_imaging-rishi-2025-06-13/config-oscar.yaml", [args.path], save_as_csv=True, batchsize=1)
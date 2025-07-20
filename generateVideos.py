import argparse
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

from read_roi import read_roi_zip


def run_ffmpeg_crop(video_path, crop, out_path, threads=4):
    x, y, w, h = crop
    cmd = [
        "ffmpeg",
        "-threads", str(threads),
        "-i", video_path,
        "-filter:v", f"crop={w}:{h}:{x}:{y}",
        "-c:a", "copy",
        "-y",  # Overwrite output
        out_path
    ]
    return subprocess.run(cmd)

def parallel_crop(video_path, roi_zip, output_folder="split_ffmpeg", max_workers=8, threads_per_job=4):
    os.makedirs(output_folder, exist_ok=True)
    rois = read_roi_zip(roi_zip)
    crops = [(roi['left'], roi['top'], roi['width'], roi['height']) for roi in rois.values()]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i, crop in enumerate(crops):
            out_path = os.path.join(output_folder, f"well_{i}.mp4")
            futures.append(executor.submit(run_ffmpeg_crop, video_path, crop, out_path, threads_per_job))

        for f in futures:
            f.result()  # Wait for all jobs

if __name__ == "__main__":
    print("Starting video cropping...")
    parser = argparse.ArgumentParser(description="Generate cropped videos from a video file using ROIs from a zip file.")
    parser.add_argument("--video", type=str, required=True, help="Path to the input video file.")
    parser.add_argument("--roi", type=str, required=True, help="Path to the zip file containing ROIs.")
    parser.add_argument("--output", type=str, required=True, help="Output folder for cropped videos.")
    args = parser.parse_args()
    parallel_crop(
        video_path=args.video,
        roi_zip=args.roi,
        output_folder=args.output,
        max_workers=8,         # Number of parallel ffmpeg processes
        threads_per_job=8      # Threads per ffmpeg process
    )

# interact -q batch -n 64 -t 02:00:00 -m 16g
# to reattach:  myq      and then       srun --jobid=<job id> --pty bash

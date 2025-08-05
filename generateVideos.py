import argparse
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

from read_roi import read_roi_zip


def build_filter_chain(x, y, w, h, roi_type):
    if roi_type != "oval":
        return f"crop={w}:{h}:{x}:{y}", False

    cx = w // 2
    cy = h // 2
    rx = w // 2
    ry = h // 2

    scale_x = ry ** 2
    scale_y = rx ** 2
    threshold = rx**2 * ry**2

    ellipse_expr = f"(pow(X-{cx}\,2)*{scale_x} + pow(Y-{cy}\,2)*{scale_y})"
    full_expr = f"lte({ellipse_expr}\,{threshold})"

    filter_complex = (
        f"[0]crop={w}:{h}:{x}:{y},format=rgba,"
        f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if({full_expr}\\,255\\,0)'[masked];"
        f"color=black@1.0:s={w}x{h}[bg];"
        f"[bg][masked]overlay=shortest=1:format=rgb"
    )

    return filter_complex, True

def run_ffmpeg_crop(video_path, crop, roi_type, out_path, threads=4):
    x, y, w, h = crop
    w = (w // 2) * 2
    h = (h // 2) * 2
    vf, is_complex = build_filter_chain(x, y, w, h, roi_type)

    cmd = [
        "ffmpeg",
        "-threads", str(threads),
        "-i", video_path,
    ]

    if is_complex:
        cmd += ["-filter_complex", vf]
    else:
        cmd += ["-vf", vf]

    cmd += [
        "-r", "30",                        # enforce constant framerate
        "-movflags", "+faststart",        # optimize for playback
        "-preset", "ultrafast",            # speed up encoding
        "-c:v", "libx264",                # ensure you're using x264
        "-c:a", "copy",                   # preserve audio
        "-y",                             # overwrite
        out_path
    ]

    print("Running:", " ".join(cmd))
    return subprocess.run(cmd)



def parallel_crop(video_path, roi_zip, output_folder="split_ffmpeg", max_workers=8, threads_per_job=4):
    os.makedirs(output_folder, exist_ok=True)
    rois = read_roi_zip(roi_zip)

    crops = []
    for name, roi in rois.items():
        crop = (roi['left'], roi['top'], roi['width'], roi['height'])
        roi_type = roi.get('type', 'rectangle').lower()
        if roi_type not in ['rectangle', 'oval']:
            print(f"Warning: Unsupported ROI type '{roi_type}', defaulting to rectangle.")
            roi_type = 'rectangle'
        crops.append((crop, roi_type))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i, (crop, roi_type) in enumerate(crops):
            out_path = os.path.join(output_folder, f"well_{i}.mp4")
            futures.append(executor.submit(run_ffmpeg_crop, video_path, crop, roi_type, out_path, threads_per_job))

        for f in futures:
            f.result()  # Wait for all jobs

if __name__ == "__main__":
    print("Starting video cropping...")
    parser = argparse.ArgumentParser(description="Generate cropped videos from a video file using ROIs from a zip file.")
    parser.add_argument("--video", type=str, required=True, help="Path to the input video file.")
    parser.add_argument("--roi", type=str, required=True, help="Path to the zip file containing ROIs.")
    parser.add_argument("--output", type=str, required=True, help="Output folder for cropped videos.")
    args = parser.parse_args()
    cpu_count = os.cpu_count() or 4
    num_cores = max(1, cpu_count // 2)
    threads_per_job = 4
    parallel_crop(
        video_path=args.video,
        roi_zip=args.roi,
        output_folder=args.output,
        max_workers=num_cores,         # Number of parallel ffmpeg processes
        threads_per_job=threads_per_job      # Threads per ffmpeg process
    )

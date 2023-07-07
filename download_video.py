import os
import sys
import subprocess

def download_video(url):
    video_format = "18"  # This will download mp4 video in 640x360 resolution
    output_template = "%(title)s.%(ext)s"  # This will name the video file as "title.mp4"

    # Build the yt-dlp command for video
    command = [
        "yt-dlp",
        "-f", video_format,
        "-o", output_template,
        url,
    ]

    # Execute the yt-dlp command
    subprocess.run(command, check=True)

    # Now we will download the srt
    output_template_srt = "%(title)s.%(ext)s"  # This will name the srt file as "title.en.srt"
    command_srt = [
        "yt-dlp",
        "--write-sub",
        "--sub-lang", "en",
        "--sub-format", "srt",
        "--convert-subs", "srt",
        "--skip-download",
        "-o", output_template_srt,
        url,
    ]

    # Execute the yt-dlp command for srt
    subprocess.run(command_srt, check=True)

    # yt-dlp appends the language code at the end of the filename, so we'll need to remove that
    video_title = subprocess.check_output(["yt-dlp", "--get-filename", "-o", "%(title)s", url])
    video_title = video_title.decode("utf-8").strip()
    original_srt_filename = f"{video_title}.en-en.srt"
    desired_srt_filename = f"{video_title}.en.srt"

    if os.path.exists(original_srt_filename):
        os.rename(original_srt_filename, desired_srt_filename)
    return desired_srt_filename

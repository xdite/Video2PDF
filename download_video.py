import subprocess
import os
import multiprocessing
from urllib.parse import urlparse, parse_qs, urlunparse
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter

def download_video(url):
    video_format = "18"  # This will download mp4 video in 640x360 resolution
    output_template = "%(title)s.%(ext)s"  # This will name the video file as "title.mp4"

    # Build the yt-dlp command
    command = [
        "yt-dlp",
        "-f", video_format,
        "-o", output_template,
        url,
    ]

    # Execute the yt-dlp command
    subprocess.run(command, check=True)

    # Get the video title
    video_title = subprocess.check_output(["yt-dlp", "--get-filename", "-o", "%(title)s", url])
    video_title = video_title.decode("utf-8").strip()
    video_filename = f"{video_title}.mp4"

    print(video_filename)
    # Call the generate_srt function



    return video_filename

def clean_url(url):
    # 解析 URL
    parsed_url = urlparse(url)
    # 清理查询字符串参数
    query = parse_qs(parsed_url.query)
    # 重建 URL
    cleaned_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        "&".join(["{}={}".format(k, v[0]) for k, v in query.items()]),
        parsed_url.fragment
    ))
    return cleaned_url

def old_generate_srt(video_filename):
    # Generate srt using whisper-ctranslate2
    num_cores = multiprocessing.cpu_count()
    print("This notebook has access to {} cores".format(num_cores))
    command_srt = [
        "whisper-ctranslate2",
        "--threads", str(num_cores) ,
        "--output_format", "srt",
        video_filename,
    ]

    # Execute the whisper-ctranslate2 command
    subprocess.run(command_srt, check=True)

def generate_srt(video_filename, video_url):
    cleaned_url = clean_url(video_url)
    command = ["yt-dlp", "--print", "id", cleaned_url]

    # Execute the command and capture the output
    process = subprocess.run(command, capture_output=True, text=True)
    # Extract the video ID from the output
    video_id = process.stdout.strip()
    transcript =YouTubeTranscriptApi.get_transcript(video_id)

    formatter = SRTFormatter()
    srt_formatted = formatter.format_transcript(transcript)

    en_srt_name = video_filename.replace("mp4", "srt")

    with open(en_srt_name, 'w', encoding='utf-8') as srt_file:
        srt_file.write(srt_formatted)

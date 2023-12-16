import csv
import subprocess
import pandas as pd
import os
from datetime import timedelta
import pysrt
import sys
from tqdm import tqdm

def detect_hardware_acceleration():
    try:
        # 尝试运行 ffmpeg 命令来列出支持的硬件加速方式
        result = subprocess.run(['ffmpeg', '-hwaccels'], capture_output=True, text=True)
        output = result.stdout

        # 检测 cuda 和 mps 支持
        if 'cuda' in output:
            return 'cuda'
        elif 'mps' in output:
            return 'mps'
    except Exception as e:
        print(f"检测硬件加速时出错: {e}")

    # 如果无法检测到支持的硬件加速，返回 None
    return None

def process_video_subs(video_path):
    base_name = os.path.splitext(video_path)[0]
    os.makedirs(base_name, exist_ok=True)

    srt_path = f'{base_name}.srt'
    if not os.path.exists(srt_path):
        print(f'找不到字幕文件: {srt_path}')
        return

    subs = pysrt.open(srt_path)

    hw_accel = detect_hardware_acceleration()

    # 使用 tqdm 包裹 subs
    for i, sub in tqdm(enumerate(subs), total=len(subs), desc="处理中"):
        start = timedelta(hours=sub.start.hours, minutes=sub.start.minutes, seconds=sub.start.seconds, milliseconds=sub.start.milliseconds)
        end = timedelta(hours=sub.end.hours, minutes=sub.end.minutes, seconds=sub.end.seconds, milliseconds=sub.end.milliseconds)
        mid_time = start + (end - start) / 2

        hours, remainder = divmod(mid_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        timestamp = '{:02}:{:02}:{:02}.{:03}'.format(hours, minutes, seconds, mid_time.microseconds // 1000)

        screenshot_filename = os.path.join(base_name, f'{i+1:04}.png')

        ffmpeg_cmd = ['ffmpeg', '-loglevel', 'error', '-ss', timestamp, '-i', video_path, '-vframes', '1', '-pix_fmt', 'yuv420p', screenshot_filename]

        if hw_accel:
            ffmpeg_cmd.insert(1, '-hwaccel')
            ffmpeg_cmd.insert(2, hw_accel)

        subprocess.run(ffmpeg_cmd)

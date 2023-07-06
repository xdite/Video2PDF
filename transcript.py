import csv
import subprocess
import pandas as pd
import os
from datetime import timedelta
import pysrt
import sys

# 取得檔名
if len(sys.argv) != 2:
    print("Usage: python script.py video_name")
    exit()

video_name = sys.argv[1]
base_name = os.path.splitext(video_name)[0]  # 去除 .mp4 後綴，取得基礎檔名

# 打開並解析 .srt 文件
subs = pysrt.open(f'{base_name}.srt')

# 建立 csv 檔
with open(f'{base_name}.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["時間點", "字幕內容", "screenshot 照片的位置"])

    for i, sub in enumerate(subs, 1):
        # 取得字幕的開始和結束時間
        start_time = timedelta(hours=sub.start.hours, minutes=sub.start.minutes, seconds=sub.start.seconds, milliseconds=sub.start.milliseconds)
        end_time = timedelta(hours=sub.end.hours, minutes=sub.end.minutes, seconds=sub.end.seconds, milliseconds=sub.end.milliseconds)

        # 計算時間中線點
        mid_time = start_time + (end_time - start_time) / 2

        # 寫入 CSV
        filename = f"{base_name}/{i:04}.png"
        writer.writerow([str(mid_time), sub.text, filename])

# 讀取 csv 檔
df = pd.read_csv(f'{base_name}.csv')

# 確保 images/ 資料夾存在
os.makedirs(base_name, exist_ok=True)

# 迴圈讀取每個時間點
for i, row in df.iterrows():
    timestamp = row['時間點']
    filename = row['screenshot 照片的位置']

    # 使用 ffmpeg 截圖
    subprocess.run(['ffmpeg', '-ss', str(timestamp), '-i', video_name, '-vframes', '1', filename])

# 儲存更新後的 csv 檔
df.to_csv(f'{base_name}.csv', index=False)

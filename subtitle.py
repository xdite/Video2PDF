import sys
from moviepy.editor import *

# 從命令行獲取MP4檔案名稱
video_file_name = sys.argv[1]
# 由MP4檔案名稱產生對應的SRT檔案名稱
subtitle_file_name = video_file_name.rsplit('.', 1)[0] + '.srt'

# Load your video
clip = VideoFileClip(video_file_name)

# Load your subtitles
with open(subtitle_file_name, "r") as f:
    subtitles = f.read()

# Split subtitles into list
subtitles = subtitles.split("\n\n")

# Process each subtitle
subs = []
for subtitle in subtitles:
    # Split by newline
    parts = subtitle.split("\n")
    if len(parts) >= 3:
        # Get start and end times
        times = parts[1].split(" --> ")
        start_time = times[0].split(":")
        end_time = times[1].split(":")
        start_time = int(start_time[0])*3600 + int(start_time[1])*60 + float(start_time[2].replace(",", "."))
        end_time = int(end_time[0])*3600 + int(end_time[1])*60 + float(end_time[2].replace(",", "."))
        # Get text
        text = " ".join(parts[2:])
        # Create text clip
        text_clip = TextClip(text, fontsize=24, color='white').set_pos(('center', 'bottom')).set_duration(end_time - start_time).set_start(start_time)
        
        subs.append(text_clip)

# Overlay subtitles on video
final = CompositeVideoClip([clip] + subs)

# Write the result to a file
final.write_videofile(video_file_name.rsplit('.', 1)[0] + '_with_subs.mp4')

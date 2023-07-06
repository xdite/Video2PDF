import os
import sys
from moviepy.editor import TextClip, ImageClip, CompositeVideoClip, VideoFileClip

def video_to_images(video_file_name: str):
    # 由MP4檔案名稱產生對應的SRT檔案名稱
    base_name = video_file_name.rsplit('.', 1)[0]
    subtitle_file_name = base_name + '.srt'

    # Load your video
    clip = VideoFileClip(video_file_name)

    # Load your subtitles
    with open(subtitle_file_name, "r") as f:
        subtitles = f.read()

    # Split subtitles into list
    subtitles = subtitles.split("\n\n")

    # 確保 images/ 目錄存在
    if not os.path.exists(base_name):
        os.makedirs(base_name)

    # Process each subtitle
    for i, subtitle in enumerate(subtitles):
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
            frame_height = clip.size[1]  # Get the height of the video frame
            text_pos = ('center', frame_height - 50)  # Calculate the position of the text

            text_clip = TextClip(text, font="楷體-簡-黑體", fontsize=21, color='yellow').set_duration(end_time - start_time).set_position(text_pos)

            # Get the frame at the start of the subtitle
            frame = clip.get_frame(start_time)
            # Create an ImageClip with this frame
            frame_clip = ImageClip(frame).set_duration(end_time - start_time)
            # Overlay the subtitle on the frame
            final = CompositeVideoClip([frame_clip, text_clip])
            # Save the frame as an image
            final.save_frame(f"{base_name}/{i:04}.png")

import os
import sys
from moviepy.editor import TextClip, ImageClip, CompositeVideoClip, VideoFileClip
from tqdm import tqdm

def video_to_images(video_file_name: str):
    base_name = video_file_name.rsplit('.', 1)[0]
    subtitle_file_name = base_name + '.srt'

    clip = VideoFileClip(video_file_name)

    with open(subtitle_file_name, "r") as f:
        subtitles = f.read()

    subtitles = subtitles.split("\n\n")

    if not os.path.exists(base_name):
        os.makedirs(base_name)

    # Wrap your loop with tqdm for a progress bar
    for i in tqdm(range(len(subtitles)), desc="Processing subtitles"):
        subtitle = subtitles[i]
        parts = subtitle.split("\n")
        if len(parts) >= 3:
            times = parts[1].split(" --> ")
            start_time = times[0].split(":")
            end_time = times[1].split(":")
            start_time = int(start_time[0])*3600 + int(start_time[1])*60 + float(start_time[2].replace(",", "."))
            end_time = int(end_time[0])*3600 + int(end_time[1])*60 + float(end_time[2].replace(",", "."))
            text = " ".join(parts[2:])
            frame_height = clip.size[1]
            # Get video width
            frame_width = clip.size[0]

            # Calculate scale factor
            scale_factor = frame_width / 1920

            # Calculate new text position and size
            text_size = 48 * scale_factor
            text_pos = ('center', frame_height - 100)

            # Create TextClip with new size and position
            text_clip = (TextClip(text, font="黑體-簡-中黑", fontsize=text_size, color='yellow', stroke_color ="black", stroke_width=0.5*scale_factor)
                .set_duration(end_time - start_time)
                .set_position(text_pos))
            frame = clip.get_frame(start_time)
            frame_clip = ImageClip(frame).set_duration(end_time - start_time)
            final = CompositeVideoClip([frame_clip, text_clip])
            final.save_frame(f"{base_name}/{i:04}.png")

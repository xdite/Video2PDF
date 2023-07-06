import os
import sys
from moviepy.editor import TextClip, ImageClip, CompositeVideoClip, VideoFileClip
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

def process_subtitle(args):
    i, zh_subtitle, en_subtitle, video_file_name, base_name = args

    clip = VideoFileClip(video_file_name)

    zh_parts = zh_subtitle.split("\n")
    en_parts = en_subtitle.split("\n")

    if len(zh_parts) >= 3 and len(en_parts) >= 3:
        times = zh_parts[1].split(" --> ")
        start_time = times[0].split(":")
        end_time = times[1].split(":")
        start_time = int(start_time[0])*3600 + int(start_time[1])*60 + float(start_time[2].replace(",", "."))
        end_time = int(end_time[0])*3600 + int(end_time[1])*60 + float(end_time[2].replace(",", "."))
        zh_text = " ".join(zh_parts[2:])
        en_text = " ".join(en_parts[2:])

        frame_height = clip.size[1]
        frame_width = clip.size[0]
        if frame_width > frame_height:
            scale_factor = frame_width / 1920
        else:
            scale_factor = frame_height / 1920

        zh_text_size = 50 * scale_factor
        en_text_size = 28 * scale_factor
        zh_text_pos = ('center', frame_height - 110)
        en_text_pos = ('center', frame_height - 57)

        zh_text_clip = (TextClip(zh_text, font="黑體-簡-中黑", fontsize=zh_text_size, bg_color='black', color='yellow', stroke_width=0.25*scale_factor)
            .set_duration(end_time - start_time)
            .set_position(zh_text_pos))

        en_text_clip = (TextClip(en_text, font="Arial", fontsize=en_text_size, color='white', bg_color='black')
            .set_duration(end_time - start_time)
            .set_position(en_text_pos))

        frame = clip.get_frame(start_time)
        frame_clip = ImageClip(frame).set_duration(end_time - start_time)
        final = CompositeVideoClip([frame_clip, zh_text_clip, en_text_clip])
        final.save_frame(f"{base_name}/{i:04}.png")

    return i


def video_to_images(video_file_name: str):
    base_name = video_file_name.rsplit('.', 1)[0]
    zh_subtitle_file_name = base_name + '.zh.srt'
    en_subtitle_file_name = base_name + '.en.srt'

    with open(zh_subtitle_file_name, "r") as f:
        zh_subtitles = f.read().split("\n\n")

    with open(en_subtitle_file_name, "r") as f:
        en_subtitles = f.read().split("\n\n")

    if not os.path.exists(base_name):
        os.makedirs(base_name)

    with Pool(cpu_count()) as pool:
        for _ in tqdm(pool.imap_unordered(process_subtitle, [(i, zh_subtitles[i], en_subtitles[i], video_file_name, base_name) for i in range(len(zh_subtitles))]), total=len(zh_subtitles)):
            pass

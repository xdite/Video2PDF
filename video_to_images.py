import os
import subprocess
import json
from moviepy.editor import TextClip, ImageClip, CompositeVideoClip, VideoFileClip
import concurrent.futures
from tqdm import tqdm

os.environ['SDL_AUDIODRIVER'] = 'dummy'

def get_video_dimensions(video_path):
    cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0",
           "-show_entries", "stream=width,height,sample_aspect_ratio", "-of", "json", video_path]
    output = subprocess.check_output(cmd).decode("utf-8")
    dimensions = json.loads(output)["streams"][0]

    width = dimensions["width"]
    height = dimensions["height"]
    sar = dimensions.get("sample_aspect_ratio", "1:1").split(":")
    sar = float(sar[0]) / float(sar[1])

    display_width = int(width * sar)
    return display_width, height

def parse_subtitle(zh_subtitle):
    zh_parts = zh_subtitle.split("\n")
    if len(zh_parts) >= 3:
        times = zh_parts[1].split(" --> ")
        start_time = times[0].split(":")
        end_time = times[1].split(":")
        start_time = int(start_time[0]) * 3600 + int(start_time[1]) * 60 + float(start_time[2].replace(",", "."))
        end_time = int(end_time[0]) * 3600 + int(end_time[1]) * 60 + float(end_time[2].replace(",", "."))
        text = " ".join(zh_parts[2:])
        return start_time, end_time, text
    else:
        return None, None, None

def process_subtitle(args):
    try:
        i, start_time, end_time, zh_text, video_file_name, base_name = args
        if start_time is None or end_time is None or not zh_text:
            return None

        clip = VideoFileClip(video_file_name)
        frame_width, frame_height = get_video_dimensions(video_file_name)

        scale_factor = frame_width / 1920 if frame_width > frame_height else frame_height / 1920
        zh_text_size = 50 * scale_factor
        zh_text_pos = ('center', frame_height - 100) if frame_width > 640 else ('center', frame_height - 30)

        font_name = "黑體-簡-中黑" if os.sys.platform == "darwin" else "Noto-Sans-Mono-CJK-SC"
        zh_text_clip = (TextClip(zh_text, font=font_name, fontsize=zh_text_size, bg_color='black', color='yellow', stroke_width=0.25*scale_factor)
                        .set_duration(end_time - start_time)
                        .set_position(zh_text_pos))

        frame = clip.get_frame(start_time)
        frame_clip = ImageClip(frame).set_duration(end_time - start_time).resize((frame_width, frame_height))

        final = CompositeVideoClip([frame_clip, zh_text_clip])
        final.save_frame(f"{base_name}/{i:04}.png")

        return i
    except Exception as e:
        print(f"Error processing subtitle index {i}: {e}")
        return None

def video_to_images(video_file_name: str):
    base_name = video_file_name.rsplit('.', 1)[0]
    zh_subtitle_file_name = base_name + '.zh.srt'

    with open(zh_subtitle_file_name, "r") as f:
        zh_subtitles = f.read().split("\n\n")

    try:
        if not os.path.exists(base_name):
            os.makedirs(base_name)
    except OSError as e:
        print(f"Failed to create directory: {base_name}. Error: {e}")
        raise
    args = []
    for i, zh_subtitle in enumerate(zh_subtitles):
        start_time, end_time, zh_text = parse_subtitle(zh_subtitle)
        args.append((i, start_time, end_time, zh_text, video_file_name, base_name))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_subtitle, arg) for arg in args]

        for f in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            pass  # 或者处理完成的 future，如：result = f.result()

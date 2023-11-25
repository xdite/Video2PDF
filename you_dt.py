import sys
import os
from download_video import download_video
from download_video import generate_srt
from translate_srt import translate_srt_file
from video_to_images import video_to_images
from convert_png_to_pdf import convert_png_to_pdf
os.environ['SDL_AUDIODRIVER'] = 'dummy'


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [youtube url]")
        sys.exit(1)

    # 擷取影片和字幕檔案
    file_name = download_video(sys.argv[1])
    generate_srt(file_name,sys.argv[1])
    # xxx.en.srt
    en_srt_name = file_name.replace("mp4", "srt")
    translate_srt_file(en_srt_name)
    # 取得影片檔案名稱和基本名稱

    video_file_name = file_name
    # xxx.en.srt => xxx.mp4

    base_name = os.path.splitext(video_file_name)[0]
    # xxx.mp4 => xxx

    # 將影片轉換為圖片
    video_to_images(video_file_name)

    # 轉換圖片為PDF
    convert_png_to_pdf(base_name, base_name)

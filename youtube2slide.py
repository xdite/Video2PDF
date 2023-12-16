import sys
import os
from download_video import download_video
from download_video import generate_srt
from download_video import old_generate_srt
from transcript import process_video_subs
from video_to_images import video_to_images
from convert_png_to_pdf import convert_png_to_pdf
from silmilar import remove_duplicate_images
os.environ['SDL_AUDIODRIVER'] = 'dummy'


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [youtube url]")
        sys.exit(1)

    # 擷取影片和字幕檔案
    file_name = download_video(sys.argv[1])
    generate_srt(file_name,sys.argv[1])

    # 取得影片檔案名稱和基本名稱

    video_file_name = file_name
    # xxx.en.srt => xxx.mp4

    base_name = os.path.splitext(video_file_name)[0]
    # xxx.mp4 => xxx

    # 將影片轉換為圖片
    # Process video subs and create screenshots
    process_video_subs(file_name) # with pre-embedd-sub
    remove_duplicate_images(base_name)
    # Convert screenshots to PDF
    convert_png_to_pdf(base_name, base_name, "_slide")

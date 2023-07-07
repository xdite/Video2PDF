import sys
from download_video import download_video
from translate_srt import translate_srt_file
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [youtube url]")
        sys.exit(1)

    file_name = download_video(sys.argv[1])
    translate_srt_file(file_name)

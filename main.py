import sys
from transcript import process_video_subs

def main():
    # 取得檔名
    if len(sys.argv) != 2:
        print("Usage: python main.py video_name")
        exit()

    video_name = sys.argv[1]
    process_video_subs(video_name)

if __name__ == "__main__":
    main()

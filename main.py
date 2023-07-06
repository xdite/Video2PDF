import sys
from transcript import process_video_subs
from book import convert_png_to_pdf

def main():
    # 取得檔名
    if len(sys.argv) != 2:
        print("Usage: python main.py video_name")
        exit()

    video_name = sys.argv[1]

    # Process video subs and create screenshots
    process_video_subs(video_name)

    # Convert screenshots to PDF
    base_name = os.path.splitext(video_name)[0]
    convert_png_to_pdf(base_name, base_name)

if __name__ == "__main__":
    main()

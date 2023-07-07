from youtube_transcript_api import YouTubeTranscriptApi
import pysrt
from datetime import timedelta

def get_srt(video_id):
    try:
        transcripts = YouTubeTranscriptApi.get_transcripts([video_id], languages=['en', 'zh-Hans'])
    except Exception as e:
        print("An error occurred: ", e)
        return

    for transcript in transcripts[0].values():
        subs = pysrt.SubRipFile()
        for i, section in enumerate(transcript):
            item = pysrt.SubRipItem()
            item.index = i
            start_seconds = section['start']
            end_seconds = start_seconds + section['duration']
            item.start = timedelta(seconds=start_seconds)
            item.end = timedelta(seconds=end_seconds)
            item.text = section['text']
            subs.append(item)

        filename = f"{video_id}.srt"
        subs.save(filename, encoding='utf-8')

        print(f"SRT file saved as {filename}.")
        return

    print("No suitable transcript found.")

# Test
video_id = "JaVBG7tFAU8"
get_srt(video_id)

import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    """
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    elif query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith('/embed/'):
            return query.path.split('/')[2]
        elif query.path.startswith('/v/'):
            return query.path.split('/')[2]
    raise ValueError("Invalid YouTube URL format.")

def transcribe_youtube_video(video_url):
    """
    Downloads transcript with timestamps from YouTube and writes it to a file.
    Returns a list of (text, start_time, duration in seconds) tuples.
    """
    video_id = extract_video_id(video_url)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except Exception as e:
        raise RuntimeError(f"Failed to fetch transcript: {str(e)}")

    os.makedirs("temp", exist_ok=True)
    output_path = "temp/transcript.txt"

    processed = []
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in transcript:
            text = entry['text'].replace('\n', ' ').strip()
            start = round(entry['start'], 2)
            duration = round(entry['duration'], 2)
            if text:
                f.write(f"[start ; {start}s  duration : {duration}s] {text}\n")
                processed.append((text, start, duration))

    return processed

if __name__ == "__main__":
    # Example usage
    video_url = "https://www.youtube.com/watch?v=LCEmiRjPEtQ"
    try:
        transcript = transcribe_youtube_video(video_url)
        for text, start , duration in transcript:
            print(f"[{start}s][{duration}s] {text}")
    except Exception as e:
        print(f"Error: {str(e)}")
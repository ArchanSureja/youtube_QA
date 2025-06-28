import nltk
from nltk.tokenize import sent_tokenize
from src.transcribe import transcribe_youtube_video

nltk.download("punkt", quiet=True)

def align_sentences_to_timestamps(transcript, merge_duration_window=300):
    """
    Merge transcript blocks into ~30s windows before applying sentence tokenizer.
    Returns a list of (sentence, start_time) with better alignment.
    """
    aligned_sentences = []

    buffer_text = ""
    buffer_start = None
    buffer_duration = 0.0
    total_chars = 0

    def flush_buffer():
        nonlocal aligned_sentences, buffer_text, buffer_start, buffer_duration, total_chars
        if not buffer_text.strip():
            return

        sentences = sent_tokenize(buffer_text.strip())
        for sentence in sentences:
            idx = buffer_text.find(sentence)
            if idx == -1 or total_chars == 0:
                continue
            proportion = idx / total_chars
            sentence_time = buffer_start + proportion * buffer_duration
            aligned_sentences.append((sentence.strip(), round(sentence_time)))
        
        # Reset buffer
        buffer_text = ""
        buffer_start = None
        buffer_duration = 0.0
        total_chars = 0

    for text, start_time, duration in transcript:
        if buffer_start is None:
            buffer_start = start_time
        buffer_text += " " + text.strip()
        buffer_duration += duration
        total_chars = len(buffer_text)

        if buffer_duration >= merge_duration_window:
            flush_buffer()

    # Flush any remaining buffer
    flush_buffer()

    return aligned_sentences

def perform_chunking(transcript, chunk_size=10, stride=3):
    """
    Returns overlapping sentence-level chunks with precise start times.
    transcript: list of (text, start_time, duration)
    """
    sentences_with_timestamps = align_sentences_to_timestamps(transcript)
    print(f"Aligned {len(sentences_with_timestamps)} sentences with timestamps.")
    chunks = []

    for i in range(0, len(sentences_with_timestamps), stride):
        window = sentences_with_timestamps[i:i + chunk_size]
        if len(window) < 2:
            continue
        chunk_text = " ".join([s[0] for s in window])
        chunk_start = window[0][1]
        chunks.append({
            "text": chunk_text,
            "start_time": chunk_start
        })

    return chunks


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=LCEmiRjPEtQ"
    try:
        transcript = transcribe_youtube_video(video_url)
        chunks = perform_chunking(transcript)
        print(f"Generated {len(chunks)} chunks:")
        for chunk in chunks:
            print(f"[{chunk['start_time']}s] {chunk['text'][:50]}...")  
    except Exception as e:
        print(f"Error: {str(e)}")

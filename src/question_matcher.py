from sentence_transformers import util
from src.transcribe import transcribe_youtube_video 
from src.chunking import perform_chunking 

def match_question_to_chunks_semantic(question_data, chunks, model,):
    """
    Given one question and list of chunks, return top_k most relevant chunk indices.
    
    Parameters:
    - question_data: text of the question
    - chunks: list of dicts with 'text' and 'start_time' keys
    - model: SentenceTransformer model
  

    Returns:
    - list of integers: indices of relevant chunks
    """
    top_k = len(chunks)//4 if len(chunks)>4 else len(chunks) 
    if not question_data or not chunks:
        return []

    chunk_texts = [chunk['text'] for chunk in chunks]

    chunk_embeddings = model.encode(chunk_texts, convert_to_tensor=True, show_progress_bar=False)
    question_embedding = model.encode(question_data, convert_to_tensor=True)

    similarities = util.cos_sim(question_embedding, chunk_embeddings)[0]
    top_indices = similarities.topk(k=top_k).indices.tolist()
    
    return top_indices

if __name__ == "__main__":
    # Example usage
    from sentence_transformers import SentenceTransformer
    video_url = "https://www.youtube.com/watch?v=LCEmiRjPEtQ"
    try:
        transcript = transcribe_youtube_video(video_url)
        chunks = perform_chunking(transcript)
        question_text = "How andrej karpathy explains the concept of new type of computing model?"
        model = SentenceTransformer("all-MiniLM-L6-v2")
        for index in match_question_to_chunks_semantic(question_text, chunks, model):
            print(f"Relevant chunk at index {index}: {chunks[index]['text']}")
    except Exception as e:
        print(f"Error: {str(e)}")
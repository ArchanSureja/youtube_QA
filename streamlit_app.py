from sentence_transformers import SentenceTransformer
import streamlit as st
from src.transcribe import transcribe_youtube_video
from src.chunking import perform_chunking 
from src.question_matcher import match_question_to_chunks_semantic
import hashlib 
from src.cache import get_cached_answer, set_cached_answer
from src.utils import get_api_key 
import google.generativeai as genai
from src.answer_generator import generate_answer

model = SentenceTransformer("all-MiniLM-L6-v2")

st.set_page_config(page_title="Ask YouTube Video", layout="wide")
st.title("Ask Questions About a YouTube Video")
st.markdown("Paste a YouTube URL and ask questions from its transcript.")


video_url = None
chunks = []

with st.form("video_form"):
    video_url = st.text_input("YouTube Video URL")
    video_submitted = st.form_submit_button("Submit Video")

if video_url and video_submitted:
    with st.spinner("Transcribing video..."):
        transcript = transcribe_youtube_video(video_url)
        chunks = perform_chunking(transcript)
    st.session_state['chunks'] = chunks
    st.session_state['video_url'] = video_url
    st.success("Transcript ready. You can now ask questions!")


if 'chunks' in st.session_state and 'video_url' in st.session_state:
    with st.form("question_form"):
        question_text = st.text_input("Ask a question")
        question_submitted = st.form_submit_button("Submit Question")

    if question_text and question_submitted:
        chunks = st.session_state['chunks']
        video_url = st.session_state['video_url']
        question_hash = hashlib.sha256(question_text.strip().encode()).hexdigest()

        with st.spinner("Finding relevant chunks..."):
            relevant_chunks = match_question_to_chunks_semantic(question_text, chunks, model)

        if not relevant_chunks:
            st.warning("No relevant context found to answer this question.")
        else:
            selected_chunks = [chunks[i]['text'] for i in relevant_chunks]
            context = " ".join(selected_chunks)
            context_hash = hashlib.sha256(context.encode()).hexdigest()
            cache_key = f"{question_hash}_{context_hash}"
            cached = get_cached_answer(cache_key)

            if cached:
                st.markdown("### Answer (from cache):")
                st.write(cached)
            else:
                with st.spinner("Generating answer..."):
                    api_key = get_api_key()
                    genai.configure(api_key=api_key)
                    gen_model = genai.GenerativeModel("gemini-2.5-flash")
                    answer = generate_answer(gen_model, context, question_text)

                if answer:
                    set_cached_answer(cache_key, answer)
                    st.markdown("### Answer:")
                    st.write(answer)

            first_chunk_index = relevant_chunks[0]
            start_time = int(chunks[first_chunk_index]['start_time'])
            minutes, seconds = divmod(start_time, 60)
            timestamp_param = f"&t={minutes}m{seconds}s" if minutes else f"&t={seconds}s"
            video_with_timestamp = video_url + timestamp_param
            st.markdown(f"[Watch this part on YouTube]({video_with_timestamp})")

import streamlit as st
from modules.uploader import handle_file_upload
from modules.summarizer import summarization_ui
from modules.chat import chat_interface

# Streamlit Page Setup
st.set_page_config(page_title="Info Retrieval System", layout="centered")
st.title("🔎 Information Retrieval System using Gemini")

# Session State Initialization
for key, default in {
    "chat_history": [],
    "doc_context": "",
    "doc_summary": "",
    "topic_summaries": {},
    "audio_outputs": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Audio format selector
st.session_state.audio_format = st.selectbox("🎵 Select Audio Format", ["mp3", "wav", "ogg"])

# Upload & Display
handle_file_upload()

# Summarization Section
summarization_ui()

# Chat Interface
chat_interface()

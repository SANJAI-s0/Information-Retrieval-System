import streamlit as st
import pyttsx3
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

def chat_interface():
    st.subheader("💬 Ask Questions from the Document")

    user_input = st.text_input(
        "Type your question here and press Enter",
        disabled=not bool(st.session_state.doc_context),
        placeholder="(Disabled until files are uploaded)"
    )

    if user_input:
        try:
            prompt = f"Using the following context, answer the question:\n\n{st.session_state.doc_context}\n\nQ: {user_input}"
            answer = model.generate_content(prompt).text.strip()
            st.session_state.chat_history.append((user_input, answer))
        except Exception as e:
            st.error(f"❌ Error: {e}")

    if st.session_state.chat_history:
        st.subheader("📝 Conversation History")
        for i, (q, a) in enumerate(st.session_state.chat_history):
            st.markdown(f"**Q{i+1}:** {q}")
            st.markdown(f"**A{i+1}:** {a}")
            st.download_button(f"💾 Download A{i+1} as TXT", a, f"chat_answer_{i+1}.txt")

            engine = pyttsx3.init()
            audio_path = f"chat_answer_{i+1}.{st.session_state.audio_format}"
            engine.save_to_file(a, audio_path)
            engine.runAndWait()
            with open(audio_path, "rb") as f:
                audio_data = f.read()
            st.audio(audio_data, format=f"audio/{st.session_state.audio_format}")
            st.download_button(f"🔊 Download A{i+1} Audio", audio_data, file_name=audio_path)

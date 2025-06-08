import streamlit as st
from fpdf import FPDF
from io import BytesIO
import pyttsx3
import os
from modules.uploader import sanitize_text
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

def summarization_ui():
    with st.expander("🧾 Summarize Uploaded Documents"):
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📃 Summarize Documents") and st.session_state.doc_context:
                with st.spinner("Summarizing..."):
                    prompt = f"Summarize the following documents:\n\n{st.session_state.doc_context}"
                    response = model.generate_content(prompt)
                    st.session_state.doc_summary = response.text.strip()
                    st.success("✅ Summary generated.")

        with col2:
            if st.button("🧹 Clear Summary"):
                st.session_state.doc_summary = ""
                st.success("Summary cleared.")

        topic = st.text_input("🔍 Enter a specific topic to summarize:")
        if st.button("📌 Summarize Topic") and topic:
            with st.spinner(f"Summarizing topic: {topic}..."):
                prompt = f"From the documents, summarize the topic '{topic}':\n\n{st.session_state.doc_context}"
                response = model.generate_content(prompt)
                topic_summary = response.text.strip()
                st.session_state.topic_summaries[topic] = topic_summary
                display_and_download(topic, topic_summary)

        if st.session_state.doc_summary:
            display_and_download("full_document_summary", st.session_state.doc_summary)

def display_and_download(label, text):
    st.subheader(f"📌 Summary: {label.replace('_', ' ').title()}")
    st.write(text)

    st.download_button("📝 Download as TXT", text, f"{label}.txt")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, sanitize_text(text))
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    pdf_output = BytesIO(pdf_bytes)
    st.download_button("📄 Download as PDF", pdf_output, f"{label}.pdf")

    engine = pyttsx3.init()
    audio_path = f"{label}.{st.session_state.audio_format}"
    engine.save_to_file(text, audio_path)
    engine.runAndWait()
    with open(audio_path, "rb") as f:
        audio_data = f.read()
    st.audio(audio_data, format=f"audio/{st.session_state.audio_format}")
    st.download_button("🔊 Download Audio", audio_data, file_name=audio_path)

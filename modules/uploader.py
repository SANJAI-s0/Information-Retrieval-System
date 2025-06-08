import streamlit as st
import PyPDF2
import docx
from unicodedata import normalize

def sanitize_text(text):
    return normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

def handle_file_upload():
    st.markdown("📂 **Upload your PDF, TXT, or DOCX files to get started**")
    uploaded_files = st.file_uploader("Upload Files", type=["pdf", "txt", "docx"], accept_multiple_files=True)
    if not uploaded_files:
        st.info("📌 *Please upload at least one file to enable question asking and summarization features.*")
        return

    combined_context = ""
    for uploaded_file in uploaded_files:
        try:
            if uploaded_file.type == "application/pdf":
                reader = PyPDF2.PdfReader(uploaded_file)
                text = ''.join(page.extract_text() for page in reader.pages)
            elif uploaded_file.type == "text/plain":
                text = uploaded_file.read().decode("utf-8")
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(uploaded_file)
                text = "\n".join([para.text for para in doc.paragraphs])
            else:
                text = ""
            combined_context += f"\n\n--- Document: {uploaded_file.name} ---\n{text.strip()}\n"
        except Exception as e:
            st.warning(f"Could not process {uploaded_file.name}: {e}")

    st.session_state.doc_context = combined_context[:8000]
    st.success(f"{len(uploaded_files)} files uploaded and processed.")

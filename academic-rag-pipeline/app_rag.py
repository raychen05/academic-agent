import streamlit as st
from rag_runner import run_rag_pipeline

st.set_page_config(page_title="Academic RAG Summarizer", layout="wide")
st.title("📚 End-to-End RAG for Academic Paper Summarization")

uploaded_file = st.file_uploader("Upload a paper (PDF or TXT)", type=["pdf", "txt"])
query = st.text_input("Enter your search query (e.g., 'novel methods for protein folding')")

if uploaded_file and query:
    with open(f"./temp/tmp_input.{uploaded_file.name.split('.')[-1]}", "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Running RAG pipeline..."):
        try:
            result = run_rag_pipeline(f.name, query)
            st.success("✅ Extracted Paper Summary:")
            st.json(result.dict())
        except Exception as e:
            st.error(f"Error: {e}")

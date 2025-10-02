import streamlit as st
from tools.paper_reader import PaperReader

# ---------------------------
# Config & init
# ---------------------------
st.set_page_config(page_title="📄 AI Paper Reader", layout="wide")
st.title("📚 AI Paper Reader")
st.write("Upload a PDF, extract sections, glossary terms, and ask AI questions!")

reader = PaperReader()

# ---------------------------
# File uploader
# ---------------------------
uploaded_file = st.file_uploader("📄 Upload a PDF", type=["pdf"])

if uploaded_file:
    with open("temp_uploaded.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # ---------------------------
    # Parse PDF
    # ---------------------------
    sections = reader.parse_pdf("temp_uploaded.pdf")

    st.subheader("📑 Sections")
    for section in sections:
        st.expander(f"Page {section['page']}").write(section["content"][:1000] + "..." if len(section["content"]) > 1000 else section["content"])

    # ---------------------------
    # Glossary terms
    # ---------------------------
    glossary = st.text_area(
        "📚 Enter glossary terms (one per line)", 
        value="neural network\ngradient descent"
    ).splitlines()

    if st.button("🔍 Extract Glossary Matches"):
        matches = reader.extract_terms(sections, glossary)
        st.subheader("✅ Glossary Matches")
        if matches:
            for term, locations in matches.items():
                st.write(f"**{term}** found in: {', '.join(locations)}")
        else:
            st.info("No matches found.")

    # ---------------------------
    # AI Q&A
    # ---------------------------
    st.subheader("🤖 Ask AI")
    question = st.text_input("Ask a question about the paper:")
    if st.button("Ask AI"):
        if question:
            answer = reader.answer_question(question, sections)
            st.write(answer)
        else:
            st.warning("Please enter a question.")



# streamlit run ui/paper_reader_app.py
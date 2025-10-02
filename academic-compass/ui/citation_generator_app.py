import streamlit as st
from tools.citation_generator import CitationGenerator
from agent.memory import MemoryManager

# ---------------------------
# Init
# ---------------------------
st.set_page_config(page_title="📑 Citation Generator", layout="centered")
st.title("📑 Citation Generator with DOI Lookup")
st.write("Generate BibTeX, APA, MLA — and store them!")

generator = CitationGenerator()
memory = MemoryManager()  # Uses your SQLite + FAISS setup

# ---------------------------
# DOI Lookup
# ---------------------------
doi_input = st.text_input("🔗 DOI (optional)", placeholder="10.1234/example.doi")

if doi_input and st.button("🔍 Fetch Metadata"):
    try:
        fetched_metadata = generator.fetch_metadata_from_doi(doi_input.strip())
        st.session_state["metadata"] = fetched_metadata
        st.success("✅ Metadata fetched!")
    except Exception as e:
        st.error(f"❌ {e}")

# ---------------------------
# Metadata Form
# ---------------------------
metadata = st.session_state.get("metadata", {})
authors = st.text_area(
    "👩‍🔬 Authors (one per line)", 
    "\n".join(metadata.get("authors", [])) if metadata else ""
)
title = st.text_input("📄 Title", metadata.get("title", ""))
journal = st.text_input("📚 Journal", metadata.get("journal", ""))
year = st.text_input("📅 Year", metadata.get("year", ""))
volume = st.text_input("📦 Volume", metadata.get("volume", ""))
number = st.text_input("🔢 Number", metadata.get("number", ""))
pages = st.text_input("📑 Pages", metadata.get("pages", ""))
doi = doi_input if doi_input else st.text_input("🔗 DOI", metadata.get("doi", ""))

# ---------------------------
# Generate & Save
# ---------------------------
if st.button("✨ Generate & Save Citations"):
    metadata = {
        "authors": [a.strip() for a in authors.splitlines() if a.strip()],
        "title": title.strip(),
        "journal": journal.strip(),
        "year": year.strip(),
        "volume": volume.strip(),
        "number": number.strip(),
        "pages": pages.strip(),
        "doi": doi.strip()
    }

    # Generate citations
    bibtex = generator.generate_bibtex(metadata)
    apa = generator.generate_apa(metadata)
    mla = generator.generate_mla(metadata)

    st.subheader("📚 Generated Citations")
    st.code(bibtex, language="bibtex")
    st.text_area("APA", value=apa, height=100)
    st.text_area("MLA", value=mla, height=100)

    # Store in MemoryManager
    full_text = f"BIBTEX:\n{bibtex}\nAPA:\n{apa}\nMLA:\n{mla}"
    embedding = [0.0] * memory.dim  # Example: use a real embedding in production!
    memory.add_to_index(full_text, embedding)
    memory.store_feedback(query=title, answer=full_text, feedback="citation", score=5)

    st.success("✅ Saved to memory!")

# streamlit run ui/citation_generator_app.py
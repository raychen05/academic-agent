# app.py

import streamlit as st
from paper_quality_estimator import PaperQualityEstimator

st.set_page_config(page_title="📚 Paper Quality Checker", layout="wide")

st.title("📚 Paper Quality Checker")
st.write("Check your papers for retractions and simple quality warnings.")

# Mocked retracted DOIs
DEFAULT_RETRACTED = [
    "10.1234/retracted123",
    "10.5678/retracted456"
]

estimator = PaperQualityEstimator(DEFAULT_RETRACTED)

# Step 1: Input papers
st.header("Step 1: Enter Paper Metadata")

num_papers = st.number_input("Number of papers to check:", min_value=1, max_value=5, value=1)

papers = []
for i in range(num_papers):
    st.subheader(f"📄 Paper {i+1}")
    doi = st.text_input(f"DOI for Paper {i+1}", key=f"doi_{i}")
    title = st.text_input(f"Title for Paper {i+1}", key=f"title_{i}")
    abstract = st.text_area(f"Abstract for Paper {i+1}", key=f"abstract_{i}")
    citation_count = st.number_input(f"Citation Count for Paper {i+1}", min_value=0, step=1, key=f"citations_{i}")
    journal = st.text_input(f"Journal Name for Paper {i+1}", key=f"journal_{i}")

    papers.append({
        "doi": doi.strip(),
        "title": title.strip(),
        "abstract": abstract.strip(),
        "citation_count": citation_count,
        "journal": journal.strip()
    })

# Check button
if st.button("🔎 Check Papers"):
    st.header("📊 Paper Quality Report")

    results = estimator.batch_estimate(papers)

    for res in results:
        st.markdown(f"### 📄 {res['title'] or res['doi'] or 'Untitled Paper'}")
        st.write(f"**DOI:** {res['doi']}")
        st.write("**Quality Checks:**")
        for warning in res['quality_warnings']:
            if "✅" in warning:
                st.success(warning)
            else:
                st.warning(warning)
        st.markdown("---")
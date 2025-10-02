# app.py

import streamlit as st
from research_gap_finder import ResearchGapFinder

st.set_page_config(page_title="Research Gap Finder", layout="wide")

st.title("🔍 Research Gap Finder")

st.markdown("""
Upload your paper abstracts, enter candidate gap topics, and generate a simple research gap report.
""")

# Upload abstracts
st.header("Step 1: Enter Paper Abstracts")
docs_input = st.text_area(
    "Paste multiple abstracts or titles (one per line):",
    placeholder="Paper abstract 1...\nPaper abstract 2..."
)

if docs_input.strip():
    docs = [line.strip() for line in docs_input.strip().split("\n") if line.strip()]
else:
    docs = []

# Candidate topics
st.header("Step 2: Enter Candidate Gap Topics")
default_candidates = [
    "explainable AI in medical imaging",
    "transfer learning for rare diseases",
    "privacy-preserving data sharing",
    "multimodal learning",
    "edge computing for real-time diagnosis"
]

candidate_input = st.text_area(
    "Enter topics to check (one per line):",
    "\n".join(default_candidates)
)

if candidate_input.strip():
    candidate_gaps = [line.strip() for line in candidate_input.strip().split("\n") if line.strip()]
else:
    candidate_gaps = []

# Button
if st.button("🔎 Generate Gap Report"):
    if not docs:
        st.error("Please enter at least one abstract.")
    elif not candidate_gaps:
        st.error("Please enter at least one candidate topic.")
    else:
        st.info("Analyzing... Please wait. ⏳")
        gap_finder = ResearchGapFinder()
        report = gap_finder.generate_gap_report(docs, candidate_gaps, top_n=10)

        st.success("✅ Analysis Complete!")

        st.subheader("📌 Extracted Keyphrases")
        st.write(", ".join(report['keyphrases']))

        st.subheader("🔬 Gap Analysis")
        for gap in report['gap_analysis']:
            st.write(f"**Topic:** {gap['topic']}")
            st.write(f"Coverage Score: `{gap['coverage_score']:.2f}`")
            st.write(f"Suggestion: {gap['gap_suggestion']}")
            st.markdown("---")
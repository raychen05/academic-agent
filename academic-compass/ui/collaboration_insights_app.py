# app.py

import streamlit as st
from tools.collaboration_insights import CollaborationInsights

st.set_page_config(page_title="🔗 Collaboration Insights", layout="wide")

st.title("🔗 Collaboration Insights")
st.write("""
Upload or enter your paper metadata to explore co-authorship trends, find top collaborators,
and get smart suggestions for new connections!
""")

# --- Step 1: Input papers ---

st.header("Step 1: Enter Paper Metadata")

num_papers = st.number_input(
    "Number of papers to include:",
    min_value=1, max_value=10, value=3
)

papers = []
for i in range(num_papers):
    st.subheader(f"📄 Paper {i+1}")

    title = st.text_input(f"Title for Paper {i+1}", key=f"title_{i}")
    authors_input = st.text_input(
        f"Authors for Paper {i+1} (comma-separated)",
        key=f"authors_{i}"
    )
    institution = st.text_input(f"Institution for Paper {i+1}", key=f"institution_{i}")

    authors = [a.strip() for a in authors_input.split(",") if a.strip()]

    papers.append({
        "title": title.strip(),
        "authors": authors,
        "institution": institution.strip()
    })

# --- Step 2: Build network ---

if st.button("🔍 Analyze Collaboration Network"):
    st.header("📊 Collaboration Insights")

    ci = CollaborationInsights(papers)

    # Institution trends
    st.subheader("🏫 Institution Trends")
    trends = ci.institution_trends()
    st.write(trends)

    # Researcher-specific insights
    st.subheader("👩‍🔬 Researcher Insights")
    researcher = st.text_input("Enter a researcher's name to get insights:", value="")

    if researcher:
        top_collabs = ci.top_collaborators(researcher)
        suggestions = ci.suggest_new_collaborators(researcher)

        st.write(f"**Top Collaborators for {researcher}:**")
        if top_collabs:
            st.write(", ".join(top_collabs))
        else:
            st.warning("No collaborators found.")

        st.write(f"**Suggested New Collaborators for {researcher}:**")
        if suggestions:
            st.write(", ".join(suggestions))
        else:
            st.info("No suggestions found.")
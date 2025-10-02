import streamlit as st
from expert_finder.core import find_experts
import pandas as pd
import json


st.set_page_config(page_title="AI Academic Expert Finder", layout="wide")
st.title("🔍 AI-Powered Academic Expert Finder")

st.markdown(
    """
    <style>
    .main {
        max-width: 80vw;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col01, col02 = st.columns([14, 2]) 
with col01:
    # Search bar
    user_input = st.text_input("🔍 Find experts in...", placeholder="quantum error correction", label_visibility="collapsed", key="search_query")
with col02:
    # Search button
    search_clicked = st.button("Search")
# Layout split
col1, col2, col3 = st.columns([1, 1, 1])

# Left Column - Top 10 Features
with col1:
    st.subheader("🚀 Top 10 Innovation Features")
    st.markdown("""
 📈 **Smart Semantic Search with Topic Matching**  
  Smart semantic search with topic matching, e.g. research questions, titles

 📌 **Multi-Source Profile Aggregation**  
  Integrates publications, funding, patents, activity, impact metrics

 🔍 **Influence & Impact Ranking (Beyond H-Index)**  
  Field-normalized citation impact, author centrality, recency

 🏛️ **AI-Powered Expert Clustering and Topic Maps**  
  Visualize topic-wise clusters, emerging themes

 🧪 **Collaboration Fit Score**  
  Based on co-authorship, org overlap, topic similarity

 🤖 **Prompt-to-Expert (LLM Assistant)**  
  Natural language interface to generate expert matches

 📅 **Expert Timeline & Trajectory Viewer**  
  Show topic shifts or rapid growth in an expert's work

 📄 **One-Click Expert Recommendation for Grant/Journal/Patent**  
  Upload title/abstract and get reviewers, collaborators

 🔍 **Context-Aware Filters**  
  Reviewer-safe, active in last 3 years, funded

 📜 **Explainable Matching**  
  Show why expert was matched: keywords, papers, impact
""")

# Right Column - Most Wanted Features
with col2:
    st.subheader("🎯 Most Wanted Search Features")
    st.markdown("""
 🎯 Natural Language Input  
 🕸️ Semantic Topic Matching  
 📊 Impact + Relevance Ranking  
 🔍 Filter by Institution, Region, Role (PI/Co-PI)  
 ⚖️ Conflict-Free Reviewer Finder  
 📤 Upload & Recommend (Title/Abstract/Proposal)  
 🗺️ Visual Exploration (maps, clusters)  
 🕸️ Recent Activity Filter  
 📥 Downloadable Profiles/Reports  
 📜 Explainability of Results  
""")


with col3:
    with st.form("expert_search_form"):
        title = st.text_input("Enter paper title or topic:", "")
        abstract = st.text_area("Paste abstract or describe your research:", "", height=200)

        col1, col2 = st.columns(2)
        with col1:
            excluded_institution = st.text_input("Exclude experts from institution:")
            preferred_region = st.selectbox(
                "Preferred Region (optional):",
                ["", "USA", "Canada", "Europe", "Asia", "Global"]
            )
        with col2:
            min_citations = st.slider("Minimum citations", 0, 5000, 100, step=50)
            top_n = st.slider("Number of top experts", 3, 20, 10)

        submitted = st.form_submit_button("🔍 Find Experts")

    if submitted:
        with st.spinner("Searching for top experts..."):
            results = find_experts(
                title=title,
                abstract=abstract,
                excluded_institution=excluded_institution,
                preferred_region=preferred_region,
                min_citations=min_citations
            )
            results = results[:top_n]

        if not results:
            st.warning("No experts matched the criteria.")
        else:
            st.success(f"Found {len(results)} expert(s).")

            # Display Results
            df_results = pd.DataFrame(results)
            for i, expert in enumerate(results):
                st.markdown(f"### {i+1}. {expert['name']} ({expert['affiliation']})")
                st.markdown(f"**Expertise**: {', '.join(expert['expertise'])}")
                st.markdown(f"**Relevance**: {expert['relevance_reason']}")
                if expert.get("conflict_risks"):
                    st.markdown(f"⚠️ **Conflicts**: {', '.join(expert['conflict_risks'])}")
                if expert.get("contact"):
                    st.markdown(f"📧 **Contact**: [{expert['contact']}](mailto:{expert['contact']})")
                st.markdown("---")

            # 🔽 Export Options
            st.markdown("## 📁 Export Results")
            export_format = st.selectbox("Select export format:", ["CSV", "JSON"])

            if export_format == "CSV":
                csv = df_results.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Download as CSV", csv, "expert_matches.csv", "text/csv")
            else:
                json_data = json.dumps(results, indent=2)
                st.download_button("⬇️ Download as JSON", json_data, "expert_matches.json", "application/json")


st.markdown("---")
# --- Display result after button press ---
if search_clicked and user_input:
    st.markdown("### Search Result")
    st.write(f"You searched for: **{user_input}**")
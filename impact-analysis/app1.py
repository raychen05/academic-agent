import streamlit as st
from services import impact_summary, citation_forecast, citation_network, patent_policy_detector, novelty_analysis, recommendation_engine

st.set_page_config(page_title="Academic Impact AI", layout="wide")

st.title("🎓 AI-Powered Academic Impact Analysis Agent")

# --- Left Sidebar for input ---
with st.sidebar:
    st.header("🔍 Select Author or Paper")
    author = st.text_input("Author Name or ORCID")
    paper_title = st.text_input("Paper Title")

# --- Top Section: Summary & Forecast ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Citation Growth & Forecasting")
    if author:
        fig = citation_forecast.plot_forecast(author)
        st.pyplot(fig)

with col2:
    st.subheader("🏆 Impact Summary")
    if author:
        summary = impact_summary.get_summary(author)
        st.metric("Citations", summary['citations'])
        st.metric("h-index", summary['h_index'])
        st.metric("Altmetrics", summary['altmetric'])

# --- Middle Section: Citation Network ---
st.subheader("🕸️ Citation Network Influence Map")
if author:
    graph_fig = citation_network.plot_network(author)
    st.pyplot(graph_fig)

# --- Bottom Section ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("🏛️ Policy & Patent Impact Detector")
    if paper_title:
        mentions = patent_policy_detector.detect(paper_title)
        st.write(mentions)

with col4:
    st.subheader("🧪 Novelty vs Impact Analyzer")
    if paper_title:
        result = novelty_analysis.analyze(paper_title)
        st.write(result)

# --- Recommendations ---
st.subheader("🎯 Targeted Impact Recommendations")
if author:
    suggestions = recommendation_engine.recommend(author)
    st.write(suggestions)

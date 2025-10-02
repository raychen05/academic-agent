import streamlit as st
from components.semantic_query import render_query_panel
from components.insight_summary import render_insights
from components.result_explorer import render_results
from components.context_tools import render_tools
from utils.semantic_search import semantic_rank
from filters.smart_filters import render_smart_filters
from utils.filter_engine import filter_papers
import json

st.set_page_config(layout="wide")
st.markdown("<h1>🔍 Academic Search Summary</h1>", unsafe_allow_html=True)

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load papers
with open("data/example-uts.json") as f:
    all_papers = json.load(f)


# Extract possible values from metadata or precomputed list
topics = sorted(set(t for p in all_papers for t in p.get("topic_clusters", [])))
domains = sorted(set(d for p in all_papers for d in p.get("application_domains", [])))

filters = render_smart_filters(topics, domains)
filtered_papers = filter_papers(all_papers, filters)


col1, col2 = st.columns([1, 2])
with col1:
    query = render_query_panel()
with col2:
    render_insights(query)

st.markdown("---")

# render_results(query)

# Semantic ranking
ranked_results = semantic_rank(query, filtered_papers)
papers_sorted = [paper for score, paper in ranked_results]

# Pass ranked list to result explorer
col3, col4 = st.columns([1, 2])
with col3:
    render_tools(query)
with col4:
    render_results(papers_sorted)

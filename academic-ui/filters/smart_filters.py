import streamlit as st

def render_smart_filters(possible_topics, domains):
    st.sidebar.header("🔎 Smart Filters")

    topic_clusters = st.sidebar.multiselect(
        "Topic Clusters",
        options=sorted(possible_topics),
        help="Filter by automatically clustered topics from abstracts"
    )

    novelty_score = st.sidebar.slider(
        "Novelty Score Range",
        min_value=0.0, max_value=1.0, value=(0.2, 0.8),
        help="Select papers with higher novelty score based on semantic uniqueness"
    )

    citation_trend = st.sidebar.selectbox(
        "Citation Trend",
        options=["Any", "Rising", "Stable", "Declining"],
        help="Trend of citations over recent years"
    )

    app_domains = st.sidebar.multiselect(
        "Application Domains",
        options=sorted(domains),
        help="Select one or more application areas"
    )

    return {
        "topics": topic_clusters,
        "novelty": novelty_score,
        "trend": citation_trend,
        "domains": app_domains
    }

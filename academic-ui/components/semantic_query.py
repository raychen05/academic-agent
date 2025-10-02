import streamlit as st

def render_query_panel():
    st.subheader("A. Semantic Query")
    query = st.text_input("Your research query", "deep learning in pathology images")

    st.markdown("**Smart Filters**")
    st.checkbox("Topic Clusters")
    st.checkbox("Novelty Score")
    st.checkbox("Influential Citations")

    st.markdown("**Query Interpretation**")
    st.code("→ computer vision, CNNs, cancer classification")

    return query

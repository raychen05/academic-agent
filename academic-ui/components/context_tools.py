import streamlit as st
from utils.author_embeddings import build_author_profile, compare_authors
from components.author_timeline import render_author_timeline
from components.topic_map import  render_topic_map
import json

def render_tools_mock(query):
    st.subheader("D. Context & Tools")

    with st.expander("🤖 CoPilot Assistant"):
        st.markdown("Ask: 'Summarize GAN classifiers in pathology'")

    with st.expander("🧠 Author Intelligence"):
        st.markdown("Top Author: Dr. J. Smith\n- Topic: Vision\n- Shifted to GANs in 2021")

    with st.expander("🕸️ Topic Map"):
        st.image("data/topic_map_example.png")

    with st.expander("⚠️ Retraction Watch"):
        st.markdown("- Paper X was flagged in 2023 (plagiarism)")


with open("data/clustered_papers.json") as f:
    clustered_papers = json.load(f)

def render_tools(query):
    st.subheader("D. Context & Tools")

    with open("data/sample_papers.json") as f:
        papers = json.load(f)

    authors = {
        "Jane Doe": [papers[0]],  # mock — normally you'd group by author
        "John Smith": [papers[0]]
    }

    with st.expander("🤖 CoPilot Assistant"):
        st.markdown("Ask: 'Summarize GAN classifiers in pathology'")
        st.text_input("Your question", "Summarize GAN classifiers in pathology")

    #with st.expander("🕸️ Topic Map"):
    #    render_topic_map(clustered_papers)

    with st.expander("⚠️ Retraction Watch"):
        st.markdown("- Paper X was flagged in 2023 (plagiarism)")

    with st.expander("📈 Author Topic Evolution"):
        author_selected = st.selectbox("Select Author", ["Jane Doe", "John Smith"])
        render_author_timeline(author_selected)   

    with st.expander("🧠 Author Intelligence"):
        selected = st.selectbox("Compare authors", list(authors.keys()))
        selected2 = st.selectbox("vs.", list(authors.keys()), index=1)

        vec1 = build_author_profile(authors[selected])
        vec2 = build_author_profile(authors[selected2])
        sim = compare_authors(vec1, vec2)

        st.markdown(f"**Similarity between** `{selected}` **and** `{selected2}`: `{sim:.2f}`")
        
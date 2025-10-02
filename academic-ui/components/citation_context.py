import streamlit as st
from utils.citation_utils import classify_citation_context

def render_citation_contexts(paper):
    st.subheader("📌 Citation Context Analysis")

    if not paper.get("citation_contexts"):
        st.info("No citation contexts available for this paper.")
        return

    for i, ctx in enumerate(paper["citation_contexts"]):
        label = classify_citation_context(ctx["text"])
        color = {
            "supporting": "✅",
            "contrasting": "⚠️",
            "background": "ℹ️"
        }.get(label, "📎")

        st.markdown(f"{color} **{label.capitalize()}** citation:")
        st.markdown(f"> {ctx['text']}")

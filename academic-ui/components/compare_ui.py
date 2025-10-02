
import streamlit as st
from utils.quick_actions import compare_two_papers
import json

# Assume this list is from prior semantic search results

with open("data/example-uts.json") as f:
    papers = json.load(f)

search_results = papers #st.session_state.get("search_results", [])

def compare_ui(k, selected_paper):
   # st.subheader("🧮 Compare with another paper")

    # Trigger popup via button
    if st.button("Compare Other Paper", key=f"compare_{k}"):
        st.session_state.show_comparison_selector = True

    # Conditional "popup" behavior
    if st.session_state.get("show_comparison_selector"):
        #with st.expander("🔍 Choose a paper to compare", expanded=True):
        paper_titles = [
            f"{i+1}. {paper['title'][:100]}..." for i, paper in enumerate(search_results)
            if paper['id'] != selected_paper['id']
        ]

        selected_index = st.selectbox(
            "Select paper to compare with:",
            options=list(range(len(paper_titles))),
            format_func=lambda i: paper_titles[i],
            key=f"compare_select_{k}"  # or any unique identifier
        )

        if st.button("Compare Now", key=f"compare_btn_{k}"):
            second_paper = [
                paper for paper in search_results if paper['id'] != selected_paper['id']
            ][selected_index]

            comparison_result = compare_two_papers(selected_paper, second_paper)
            st.session_state["comparison_result"] = comparison_result
            st.session_state["show_comparison_selector"] = False



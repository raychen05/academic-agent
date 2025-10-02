import streamlit as st
import json
from utils.llm_helpers import summarize_paper
from utils.citation_utils import classify_citation_context
from utils.quick_actions import *
from components.citation_context import render_citation_contexts
from components.compare_ui import compare_ui
from components.topic_map import  render_topic_map

with open("data/clustered_papers.json") as f:
    clustered_papers = json.load(f)

with open("data/example-uts.json") as f:  # sample_papers
    papers = json.load(f)

if 'search_results' not in st.session_state:
    st.session_state["search_results"] = papers

per_page = 5
if 'page' not in st.session_state:
    st.session_state["page"]  = 1
    
if 'reading_list' not in st.session_state:
    st.session_state["reading_list"] = []

if "summaries" not in st.session_state:
    st.session_state["summaries"] = {}

if "citation_results" not in st.session_state:
    st.session_state["citation_results"] = {}


def format_json_to_markdown(data):
    lines = []
    for key, value in data.items():
        # If value is a list of lists, flatten it
        if isinstance(value, list) and len(value) == 1 and isinstance(value[0], list):
            value = value[0]
        value_str = ", ".join(f"`{v}`" for v in value)
        lines.append(f"**{key}**: {value_str}")
    return "\n\n".join(lines)

def render_results_mock(query):
    st.subheader("C. Smart Result Explorer")

    for i in range(2):  # mock two results
        with st.expander(f"📄 Paper Title {i+1}"):
            st.markdown("**Highlights**: Proposed new loss function for segmentation")
            st.markdown("- Citation Context: _Supportive_")
            st.markdown("- Retraction Flag: ❌ No")
            st.markdown("- Scientific Claims: 'Improved accuracy by 8%'")

            st.button("💬 Ask AI to Summarize", key=f"sum_{i}")
            st.button("📊 Compare with another", key=f"cmp_{i}")

def render_results(query):
    st.subheader("C. Smart Result Explorer")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Paper Details", "🤖 CoPilot Assistant", "⚡ Quick Actions Output", "🕸️ Topic Map"])

    with tab1:
        if 'page' not in st.session_state:
            st.session_state["page"]  = 1
        start = (st.session_state.page - 1) * per_page
        end = start + per_page

        for i, paper in enumerate(papers[start:end]):
            with st.expander(f"###### 📄 {paper['title']}"):
                st.markdown(f"**Abstract**: {paper['abstract']}")
                st.markdown("**Citation Contexts:**")

                for ctx in paper["citation_contexts"]:
                    label = classify_citation_context(ctx["text"])
                    st.markdown(f"• **_{label.capitalize()}_**: {ctx['text']}")
                    
                st.markdown(f"**Retraction Flag**: {'✅' if paper.get('retracted') else '❌'}")
                st.markdown(f"**Scientific Claims**: {paper.get('claims', 'No claims available')}")

                render_citation_contexts(paper)
             
                col_a1, col_a2, col_a3, col_a4 = st.columns(4)
                with col_a1:
                    if st.button("💬 Ask AI to Summarize", key=f"sum_{i}", use_container_width=True):
                        with st.spinner("Summarizing..."):
                            summary = summarize_paper(paper["title"], paper["abstract"])
                            st.session_state.summaries[paper["id"]] = summary

                if paper["id"] in st.session_state.summaries:
                    st.success("✅ Summary:")
                    st.markdown(st.session_state.summaries[paper["id"]])

                with col_a2:
                    if st.button("➕ Add to Reading List", key=f"add_{i}",  use_container_width=True):
                        if paper["id"] not in st.session_state.reading_list:
                            st.session_state.reading_list.append(paper["id"])
                        
                if paper["id"] in st.session_state.reading_list:
                    st.success("📚 In your reading list")
                    st.markdown(st.session_state.reading_list)

                with col_a3:
                    compare_ui(i, paper)
                   # if st.button("🧮 Compare Other Paper", key=f"cmp_{i}", use_container_width=True):
                   #     st.warning("Comparison not available – select another paper to compare.")
                    # Display comparison if available
                if "comparison_result" in st.session_state:

                    st.success("🔍 Comparison Summary")
                    #st.markdown("#### 🔍 Comparison Summary")
                   # markdown_output = "\n\n".join(
                   #        f"**{key}:** {value}" for key, value in st.session_state["comparison_result"].items()
                #    )
                    st.write(st.session_state["comparison_result"])

                with col_a4:
                    if st.button("🧵 Follow Citation Path", key=f"cit_{i}", use_container_width=True):
                        result = follow_citation_path(paper)
                        st.session_state.citation_results[paper["id"]] = result

                if paper["id"] in st.session_state.citation_results:
                    st.success("🔗 Citation Path")
                    st.markdown(st.session_state.citation_results[paper["id"]])
                    # formatted_md = format_json_to_markdown(st.session_state.citation_results[paper["id"]])
                    #st.markdown(formatted_md)
                    # st.markdown("- Builds on: Doe et al. 2020\n- Cited by: Smith et al. 2024")
            

        col1, col2 = st.columns(2)

        with col1:
            if st.button('Previous') and st.session_state.page > 1:
                st.session_state.page -= 1
        with col2:
            if st.button('Next') and end < len(papers):
                st.session_state.page += 1

    with tab2:
            st.markdown("### 🤖 CoPilot Assistant")
            question = st.text_input("Ask about this paper:")
            if question:
                # Replace this with real LLM call
                st.success(f"**You asked:** {question}")
                st.info("🔎 _LLM Answer Placeholder: This model accelerates discovery by modeling molecular structures with attention._")

    with tab3:
        st.markdown("### ⚡ Quick Actions")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✍️ Summarize in Plain English"):
                st.info("_This paper introduces a smarter way to find new drugs using AI models called transformers._")

        with col2:
            st.markdown("**Placeholder for Additional Actions**:")

    with tab4:
        render_topic_map(clustered_papers)
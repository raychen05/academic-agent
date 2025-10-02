import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from services import impact_summary, antargetis_impact, citation_network, citation_graph_influence, patent_policy_detector, novelty_analysis, targeted_impact
#from services.citation_forecast import plot_forecast
from components import memory, antargetis_ui, novelty_ui, targeted_impact_ui, metric_card, profile_card, patent_impact_ui, citation_forecast_ui, collab_impact_ui, knowledge_diffusion_ui, concept_adoption_ui, interdisciplinary_bridging_ui

st.set_page_config(layout="wide")
st.title("AI-Powered Academic Impact Analysis Agent")

st.markdown("""
    <style>
    .main {
        max-width: 80vw;
        margin-left: auto;
        margin-right: auto;
    }
    .card {
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    .card h3 {
        margin-top: 0;
    }
    .benchmark-note {
        font-style: italic;
        color: #666;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)
      
# --- Left Sidebar for input ---
with st.sidebar:
    st.header("🔍 Select Author or Paper")
    author = st.text_input("Author Name or ORCID")
    paper_title = st.text_input("Paper Title")

    name = memory.get_value("author")
    if not name or name != author:
        memory.set("author", author)
        memory.clear_all()  # Clear previous data when author changes

# --- LEFT COLUMN (Main features & Graphs) ---
left, right = st.columns([1, 1])

with left:
    with st.container(border=True):
        st.subheader("👤 Researcher Profile")
        if author:
            meta_summary = memory.get_object("author_profile")
            if not meta_summary or meta_summary.get("name") != author:
                meta_summary = impact_summary.get_meta_summary(author)
                memory.set_object("author_profile", meta_summary)
            profile_card.render_author_card(meta_summary)


    with st.container(border=True):
        st.subheader(" 📈 Citation Growth & Forecasting")
        st.markdown("Predict future citation trajectories for papers, researchers, or institutions.")
        if author:
            name = memory.get_value("author")
            if not name or name != author:
                memory.set("author", author)
            citation_forecast_ui.plot_forecast(author)


    with st.container(border=True):
        # --- Input field + button (same row) ---
        st.subheader("🌍 Policy & Patent Impact Detector")
        st.markdown("Detect if a paper has been cited in government policies, patents, or other real-world applications.")
        st.markdown("This feature helps identify the practical impact of research beyond academia.")
    
        #col1, col2 = st.columns([4, 1])
        #with col1:
        #    paper_title = st.text_input("Has the paper been cited in government policy, patents, etc?", label_visibility="collapsed", placeholder='e.g. "Deep Neural Networks for NLP"')
        #with col2:
        #    check_btn = st.button("🔍")
        
        #if paper_title:
        #    mentions = patent_policy_detector.detect(paper_title)
        #    st.write(mentions)
        
        patent_impact_data = memory.get_object("patent_impact")
        if not patent_impact_data:
            patent_impact_data = patent_impact_ui.get_mock_input()
            memory.set_object("patent_impact", patent_impact_data)
        patent_impact_ui.render_impact_detector(patent_impact_data)


    with st.container(border=True):
        st.subheader ("🔎 Novelty vs Impact Analyzer")
        st.markdown("Analyze the novelty of a paper and its potential impact on policy, patents, and industry.")
        st.markdown("This feature helps assess how unique and impactful a research idea is.")
        #if paper_title:
        novelty_analysis_data = memory.get_json("novelty_analysis")
        if not novelty_analysis_data:
            novelty_analysis_data = novelty_ui.get_mock_input()
            memory.set_json("novelty_analysis", novelty_analysis_data )
        novelty_ui.render_novelty_analysis(novelty_analysis_data)

        # result = novelty_analysis.analyze(paper_title)
        #st.write(result)
        # st.success(f"'{paper_title}' has **not** yet been cited in policies or patents.")  # Mock response
    with st.container(border=True):
        st.subheader(" 🔗 Collaborator Impact Attribution")
        st.markdown("Enter paper metadata and view attribution across authors, institutions, and grants.")

        collab_impact_ui.render_collab_impact_attribution()

    with st.container(border=True):
        st.subheader("🧠 Concept Adoption Index")
        st.markdown("Detect novel terms/methods from a paper and measure how often they are reused in subsequent publications.")

        concept_adoption_ui.render_concept_adoption_ui()


    with st.container(border=True):
        st.subheader(" 🔀 Interdisciplinary Bridging Explorer")
        st.markdown("Measure how well a paper connects distant fields based on the fields of citing papers.")
        interdisciplinary_bridging_ui.render_bridging_ui()

# --- RIGHT COLUMN (Summary + Recommendation) ---
with right:
    with st.container(border=True):
        st.subheader("🧠 Impact Summary & Benchmarking")
        st.markdown("Get a comprehensive summary of an author's impact, including citation metrics, publication trends, and field influence.")
        st.markdown("This feature provides a holistic view of an author's academic contributions and influence.")

        st.markdown("*Benchmarked: `amg.mig` austber peers in Computer Science*")
        if author:
            col1, col2, col3 = st.columns(3)
            summary_data = memory.get_object("impact_summary")
            if not summary_data or summary_data.get("author") != author:
                summary_data = impact_summary.get_summary(author)
                memory.set_object("impact_summary", summary_data)
            metric_card.render_metric_card(summary_data)

            # Horizontal bar chart (mocked comparison)
            st.progress(0.85, text="Top Peers")
            st.progress(0.55, text="You")


    with st.container(border=True):
        st.subheader("🕸️ Citation Network Influence Map")
        st.markdown(" Predict future citation trajectories for papers, researchers, or institutions.")

        if author:
            citation_network_data = memory.get_object("citation_network")
            if not citation_network_data :
                memory.set_object("citation_network", citation_network_data)
            graph_fig = citation_network.plot_network(author)
            st.pyplot(graph_fig)

    with st.container(border=True):
        st.subheader("🤖 Citation Network Influence Score")
        if author:
            citation_graph_influence_data = memory.get_object("citation_graph_influence")
            if not citation_graph_influence_data :
                memory.set_object("citation_graph_influence", citation_graph_influence_data)
            citation_graph_influence.plot_citation_influence_score()


    with st.container(border=True):
        st.subheader("🧠 Antargetis Impact Recommendations")
        st.markdown(" Recommend targeted audiences and sectors that can most benefit from or amplify the impact of a research paper or idea.")
        #if st.button("Analyze Antargetis Impact"):
        antargetis_data = memory.get_json("antargetis_impact")
        if not antargetis_data:
            antargetis_data = antargetis_impact.recommend_targets(
                title="Machine Learning-Guided Discovery of Antiviral Peptides for Emerging RNA Viruses",
                abstract="This paper presents a deep learning framework to identify novel antiviral peptides...",
                keywords=["antiviral", "peptides", "machine learning", "RNA viruses", "drug discovery"]
            )
            memory.set_json("antargetis_impact", antargetis_data)
        antargetis_ui.render_antargetis_card(antargetis_data)


    with st.container(border=True):
        st.subheader("🎯 Targeted Impact Recommendations")
        st.markdown("Recommend actions to increase impact (venues, collaborations, topics, dissemination).")

        # if st.button("Analyze Targeted Impact"):
        suggestions = targeted_impact.recommend_impact_strategy(
            title="A Transformer-based Framework for Predicting Plant Disease Resistance Genes",
            abstract="We propose a deep learning architecture that uses genomic sequences...",
            keywords=["genomics", "plant breeding", "transformers", "crop disease", "deep learning"],
            author_affiliation="University of California, Davis",
            field="Agricultural Genomics"
        )
        recommend_mock = memory.get_json("targeted_impact")
        if not recommend_mock:
            recommend_mock = targeted_impact_ui.recommend_mock(author)
            memory.set_json("targeted_impact", recommend_mock)
        targeted_impact_ui.render_targeted_impact(recommend_mock)


        ##st.write(suggestions)
        #st.markdown(f"##### Recommendations for **{author}**")
        #for rec in suggestions:
        #    st.markdown(f"&emsp;&emsp;✅ {rec}", unsafe_allow_html=True)


    with st.container(border=True):
        st.subheader("🌐 Knowledge Diffusion Score")
        st.markdown("Measure how far and wide a paper's core ideas spread across disciplines, geographies, languages, and time.")
        knowledge_diffusion_ui.render_knowledge_diffusion_ui()
import streamlit as st
from utils.llm_helpers import generate_insight_summary
import json
import altair as alt
import pandas as pd
import plotly.express as px

def render_insights_mock(query):
    eft_panel, right_panel = st.columns([1, 2])
    with eft_panel:
        st.subheader("B. Insight Summary")
        st.markdown("> GANs are increasingly used for data augmentation...")
        st.markdown("**Key Findings:**")
        st.markdown("- Top methods: CycleGAN, StyleGAN")
        st.markdown("- Common datasets: TCGA, Camelyon16")
    with right_panel:
            st.markdown("**Citation Trends**")
            st.line_chart({"2021": 12, "2022": 24, "2023": 58})


def render_insights(query):
    st.subheader("B. Insight Summary")

    with open("data/example-uts.json") as f:
        papers = json.load(f)

    left_panel, right_panel = st.columns([1, 1])
    with left_panel:
        if st.button("🧠 Generate LLM Insight Summary"):
            with st.spinner("Analyzing papers..."):
                summary = generate_insight_summary(papers)
                st.markdown(summary)
        
        st.markdown("**Key Findings:**")
        st.markdown("- Top methods: CycleGAN, StyleGAN")
        st.markdown("- Common datasets: TCGA, Camelyon16")
        st.markdown("- Top Keywords: Data Augmentation, GANs, Medical Imaging")

        # Topic selector for trend charts
        trend_option = st.radio(
            "Select a trend to display:",
            ["Citation", "Method Usage", "Dataset", "Keyword"],
            index=0,
            key="trend_selector"
    )

    with right_panel:

        # Sample trend data
        if trend_option == "Citation":
            data = {"2021": 12, "2022": 24, "2023": 58}
        elif trend_option == "Method Usage":
            data = {"2021": 3, "2022": 10, "2023": 22}
        elif trend_option == "Dataset":
            data = {"2021": 2, "2022": 8, "2023": 15}
        elif trend_option == "Keyword":
            data = {"2021": 5, "2022": 9, "2023": 18}
        else:
            data = {}

        st.markdown(f"**{trend_option}**")
        df = pd.DataFrame.from_dict(data, orient="index", columns=["Count"])
        df.index.name = "Year"
        st.line_chart(df)

       # st.markdown("**Citation Trends**")
       # st.line_chart({"2021": 12, "2022": 24, "2023": 58})

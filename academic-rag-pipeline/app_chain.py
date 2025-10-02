import streamlit as st
from chain import chain
from pdf_extractor import extract_text_from_pdf, extract_structured_sections

st.set_page_config(page_title="Academic Paper Extractor", layout="wide")
st.title("📄 Academic Paper Summary Extractor")


with st.sidebar:
    st.header("Upload Paper Info")
    uploaded_file = st.file_uploader("Upload a CSV, JSON, or PDF file (title + abstract)", type=["csv", "json", "jsonl", "pdf"])
    run_button = st.button("🚀 Extract Insights")

if run_button and uploaded_file:
    import pandas as pd
    import json

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".json"):
            df = pd.DataFrame(json.load(uploaded_file))
            #  df = pd.read_json(uploaded_file)
        elif uploaded_file.name.endswith(".jsonl"):
            df = pd.DataFrame([json.loads(line) for line in uploaded_file])
        elif uploaded_file.name.endswith(".pdf"):
            raw_text = extract_text_from_pdf(uploaded_file)
            structured = extract_structured_sections(raw_text)
            df = pd.DataFrame([structured])

        for idx, row in df.iterrows():
            with st.expander(f"📘 {row['title']}", expanded=False):
                with st.spinner("Extracting..."):
                    try:
                        response = chain.run({
                            "paper_title": row['title'],
                            "paper_abstract": row['abstract']
                        })

                        st.markdown("### 🧠 Summary")
                        st.markdown(f"**Objective**: {response.objective}")
                        st.markdown(f"**Method**: {response.method}")
                        st.markdown(f"**Results**: {response.results}")
                        st.markdown(f"**Contributions**: {response.contributions}")
                        st.markdown(f"**Datasets**: {', '.join(response.datasets)}")
                        st.markdown(f"**Tools**: {', '.join(response.models_or_tools)}")
                        st.markdown(f"**Metrics**: {', '.join(response.evaluation_metrics)}")
                        st.markdown(f"**Keywords**: {', '.join(response.keywords)}")
                        st.markdown(f"**Paper Type**: {response.paper_type}")
                        st.markdown(f"**Lay Summary**: {response.lay_summary}")

                        with st.expander("📊 Full Extracted JSON"):
                            st.json(response.dict())

                    except Exception as e:
                        st.error(f"Failed to extract paper: {e}")

    except Exception as e:
        st.error(f"Error loading file: {e}")
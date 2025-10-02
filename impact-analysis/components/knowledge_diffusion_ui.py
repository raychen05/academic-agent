import streamlit as st
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from services.diffusion import fetch_citations, compute_knowledge_diffusion_score
from services.llm_helpers import call_llm


def get_diffusion_in_mock():
    return {
        "paper": {
            "title": "A Transformer-based Approach for Quantum Chemistry",
            "abstract": "We propose a transformer architecture that replaces density functional theory...",
            "year": 2022,
        "doi": "10.1000/example"
        },
        "citations": [
            {
            "title": "Follow-up transformer chemistry",
            "abstract": "...",
            "year": 2023,
            "venue": "Chem AI",
            "affiliations": [{"institution":"Univ X","country":"US"}],
            "language": "en"
            },
            {
            "title": "应用变换器在量子化学中的实现",
            "abstract": "...",
            "year": 2024,
            "venue": "中国化学杂志",
            "affiliations": [{"institution":"Univ Y","country":"CN"}],
            "language": "zh"
            }
        ]
    }

def get_diffusion_out_mock():
    return {
        "paper": {"title":"A Transformer-based Approach for Quantum Chemistry","doi":"10.1000/example","year":2022},
        "n_citations": 2,
        "components": {
            "breadth": {"value": 0.56, "discipline_counts":{"Chemistry":1,"Other":1}, "discipline_entropy_norm":0.56, "n_disciplines":2},
            "geography": {"value":0.5,"country_counts":{"US":1,"CN":1},"country_entropy_norm":0.5,"n_countries":2,"coverage":0.6667},
            "language": {"value":0.0,"language_counts":{"en":1,"zh":1},"language_entropy_norm":0.5,"n_languages":2},
            "depth": {"value":0.38,"avg_distance":0.38,"p90_distance":0.6},
            "temporal": {"value":0.25,"early_share":0.8,"median_year":2023}
        },
        "weights": {"breadth":0.3,"geo":0.2,"lang":0.1,"depth":0.25,"temporal":0.15},
        "diffusion_score": 45.12,
        "coords": [[0.0,0.0],[0.2,-0.1],[-0.3,0.2]],
        "labels": [0,1,1]
        }

def classify_papers_llm(papers):
    """
    Classify papers into a single discipline based on their title and abstract.
    
    Args:
        papers (list of dict): Each dict must have keys "id", "title", and "abstract".
        Example:
        [
            {"id": 1, "title": "Paper title", "abstract": "Paper abstract"},
            {"id": 2, "title": "Another title", "abstract": "Another abstract"}
        ]
    
    Returns:
        str: The LLM's JSON output as a string.
    """
    # Build the input list for the prompt
    paper_texts = []
    for paper in papers:
        paper_texts.append(
            f"{paper['id']}) Title: {paper['title']}\n   Abstract: {paper['abstract']}"
        )
    
    # Join the paper descriptions
    paper_section = "\n".join(paper_texts)
    
    # Create the LLM prompt
    prompt = f"""
You are an expert research classifier. Given the title and abstract of a paper, return a single-discipline label 
(e.g., "Chemistry", "Physics", "Computer Science", "Biology", "Engineering", "Medicine", "Economics", "Policy") 
that best fits the paper. If mixed, return the primary discipline.

Input:
{paper_section}

Return JSON:
[
  {{"id": 1, "discipline": "Chemistry"}},
  {{"id": 2, "discipline": "Computer Science"}}
]
"""
    return call_llm(prompt)


def explain_diffusion_scores_llm(diffusion_data):
    """
    Generate a concise 2–3 sentence explanation of a paper's diffusion score
    based on breadth, geography, depth, language, and temporal components.
    
    Args:
        diffusion_data (dict): A dictionary with keys:
            - diffusion_score (float)
            - components (dict with sub-keys for breadth, geography, language, depth, temporal)
            - n_citations (int)
    
    Returns:
        str: LLM-generated paragraph explaining diffusion.
    """
    import json
    
    # Convert the diffusion_data dict to a formatted JSON string
    diffusion_json = json.dumps(diffusion_data, indent=2)
    
    # Build the prompt
    prompt = f"""
You are an expert science communicator. Given the following diffusion component values for a paper,
produce a concise 2–3 sentence explanation summarizing how widely and how quickly the paper's ideas have spread,
and what the main driver is (breadth, geography, depth, language).

Input JSON:
{diffusion_json}

Produce a short paragraph (2-3 sentences).
"""
    return call_llm(prompt)



def render_knowledge_diffusion_ui():

    with st.expander("Paste paper JSON (or use demo)"):
        sample_json = {
            "paper": {"title":"A Transformer-based Approach for Quantum Chemistry","abstract":"We propose a transformer architecture...","year":2022,"doi":"10.1000/example"},
            "paper_id": "demo:1"
        }
        st.code(sample_json, language="json")

    col1, col2 = st.columns([2,1])
    with col1:
        title = st.text_input("Paper Title", key="title", value=sample_json["paper"]["title"])
        abstract = st.text_area("Abstract", key="abstract", value=sample_json["paper"]["abstract"], height=120)
        year = st.number_input("Year", key="year", value=sample_json["paper"]["year"])
        doi = st.text_input("DOI (optional)", key="doi", value=sample_json["paper"].get("doi",""))
        paper = {"title": title, "abstract": abstract, "year": year, "doi": doi}
        analyze = st.button("Analyze Diffusion")

    with col2:
        st.markdown("### Options")
        st.write("Model: all-MiniLM-L6-v2 (local)")
        st.write("Projection: PCA")
        st.write("Clustering: KMeans")

    if analyze:
        with st.spinner("Fetching citations and computing diffusion..."):
            # In production: fetch from OpenAlex / Semantic Scholar / internal datastore
            citations = fetch_citations(doi or title)
            res = compute_knowledge_diffusion_score(paper, citations)

        # Top card
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2,1,1])
        with c1:
            st.subheader(res["paper"]["title"])
            st.markdown(f"**DOI:** {res['paper'].get('doi','-')}")
            st.markdown(f"**Citations considered:** {res['n_citations']}")
        with c2:
            st.metric("Knowledge Diffusion Score", f"{res['diffusion_score']} / 100")
        with c3:
            # small breakdown
            comps = res["components"]
            st.markdown("**Top components**")
            st.write(f"• Breadth: {comps['breadth']['value']:.2f}")
            st.write(f"• Geography: {comps['geography']['value']:.2f}")
            st.write(f"• Depth: {comps['depth']['value']:.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # Two-column visualizations
        v1, v2 = st.columns([2,1])

        # Topic scatter: coords
        coords = np.array(res["coords"])
        labels = np.array(res["labels"])
        # first point is the paper (index 0)
        paper_pt = coords[0]
        cite_pts = coords[1:] if coords.shape[0]>1 else np.empty((0,2))

        with v1:
            st.subheader("Topic Map (paper + citations)")
            fig, ax = plt.subplots(figsize=(6,5))
            if cite_pts.shape[0]>0:
                ax.scatter(cite_pts[:,0], cite_pts[:,1], c='gray', alpha=0.6, s=50, label='Citations')
            ax.scatter(paper_pt[0], paper_pt[1], c='red', s=140, edgecolors='black', label='Paper')
            # annotate a few
            ax.set_xlabel("Topic dim 1")
            ax.set_ylabel("Topic dim 2")
            ax.legend()
            ax.grid(alpha=0.2)
            st.pyplot(fig)

        with v2:
            st.subheader("Discipline Spread")
            disc_counts = res["components"]["breadth"]["discipline_counts"]
            if disc_counts:
                disc_df = pd.DataFrame(list(disc_counts.items()), columns=["discipline","count"]).sort_values("count", ascending=False)
                st.bar_chart(disc_df.set_index("discipline"))
            else:
                st.write("No discipline data available")

        st.markdown("---")
        b1, b2 = st.columns(2)
        with b1:
            st.subheader("Geographic Spread")
            country_counts = res["components"]["geography"]["country_counts"]
            if country_counts:
                cdf = pd.DataFrame(list(country_counts.items()), columns=["country","count"]).sort_values("count", ascending=False)
                st.table(cdf.head(10))
            else:
                st.write("No country data")

        with b2:
            st.subheader("Temporal Diffusion")
            t = res["components"]["temporal"]
            st.write(f"Early share (first 2 years): {t['early_share']:.2f}")
            st.write(f"Median citing year: {t['median_year']}")

        st.markdown("---")
        st.subheader("Component details")
        st.json(res["components"])

        # Download JSON
        st.download_button("Download detailed diffusion JSON", json.dumps(res, indent=2), file_name="diffusion_result.json")



from services.concept_adoption  import compute_concept_adoption, build_candidate_concepts
import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from services.llm_helpers import call_llm


def compute_concept_adoption_mock():
    paper = {
        "title": "Transformer-Accelerated Reaction Prediction",
        "abstract": "We introduce TransReact, a transformer-based architecture that predicts catalytic reaction pathways with a novel loss function 'react-loss' that improves selectivity.",
        "year": 2022,
        "doi": "10.1000/transreact"
    }

    # demo citations: in production you would fetch OpenAlex/Semantic Scholar citing papers
    citations = [
        {"title": "Applying TransReact to Photocatalysis", "abstract":"We use TransReact and react-loss ...", "year":2023, "text": "We use TransReact and the react-loss introduced by ..."},
        {"title": "A Survey of reaction predictors", "abstract":"This survey discusses TransReact among others", "year":2024, "text": "TransReact ..."},
        {"title": "Transformer models in catalysis", "abstract":"No direct reuse", "year":2023, "text": "This paper mentions transformers but not TransReact specifically."}
    ]

    res = compute_concept_adoption(paper, citations)
    print(json.dumps(res, indent=2))
    return res


def get_concept_adoption_summary_mock():
    return {
        "paper": {"title":"Transformer-Accelerated Reaction Prediction","doi":"10.1000/transreact","year":2022},
        "n_candidates": 12,
        "n_citations": 3,
        "cai": 42.18,
        "concepts": [
            {
            "concept":"transreact",
            "exact_count":2,
            "semantic_count":0,
            "total_matches":2,
            "first_year":2023,
            "years":[2023,2024],
            "velocity":1.0,
            "matched_docs":[{"meta": {"title":"Applying TransReact to Photocatalysis","year":2023}, "exact_matches":1, "semantic_match":false}, ...]
            },
            {
            "concept":"react-loss",
            "exact_count":1,
            "semantic_count":1,
            "total_matches":2,
            "first_year":2023,
            "years":[2023,2024],
            "velocity":1.0
            }
        ]
        }


def explain_concept_adoption_llm(concept_adoption_data):
    """
    Generate a 3–4 sentence summary of a Concept Adoption analysis.

    Args:
        concept_adoption_data (dict): The JSON output from the Concept Adoption analysis.

    Returns:
        str: LLM-generated plain-text explanation.
    """
    import json

    # Convert the input dict to nicely formatted JSON for the prompt
    concept_json = json.dumps(concept_adoption_data, indent=2)

    # Build the prompt
    prompt = f"""
You are an expert science communicator. Given this Concept Adoption analysis output (JSON),
produce a concise 3–4 sentence summary describing:
- whether the paper introduced concepts that are being reused,
- which concepts are most adopted,
- how quickly adoption occurred,
- any caveats (small sample, semantic matches).

Input:
{concept_json}

Output: 2-4 sentences, plain text.
    """
    return call_llm(prompt)

def assess_novel_concept_llm(phrase):
    """
    Ask the LLM to assess whether a phrase is likely a novel concept or an existing term.

    Args:
        phrase (str): The phrase or term to evaluate.

    Returns:
        str: JSON string from the LLM with keys:
             - phrase (str)
             - likely_novel (bool)
             - explanation (str)
    """
    # Build the prompt
    prompt = f"""
You are a research librarian. Given a short phrase or term, determine whether it likely represents a novel concept (coinage)
or an existing common term.

Return JSON:
{{"phrase":"...", "likely_novel": true/false, "explanation":"2-sentence justification and suggested search keywords to verify"}}.

Phrase: "{phrase}"
"""
    return call_llm(prompt)

   
def render_concept_adoption_ui():
  
    with st.expander("Sample paper"):
        st.code({
            "title": "Transformer-Accelerated Reaction Prediction",
            "abstract": "We introduce TransReact, a transformer-based architecture... introduces 'react-loss' as a novel objective.",
            "year": 2022
        }, language="json")

    col1, col2 = st.columns([3,1])
    with col1:
        title = st.text_input("Paper Title", value="Transformer-Accelerated Reaction Prediction")
        abstract = st.text_area("Abstract", value="We introduce TransReact, a transformer-based architecture that predicts catalytic reaction pathways with a novel loss function 'react-loss' that improves selectivity.", height=160)
        year = st.number_input("Year", value=2022, min_value=1900, max_value=2100)
        doi = st.text_input("DOI (optional)")
        paper = {"title": title, "abstract": abstract, "year": year, "doi": doi}

        st.markdown("### Citing papers (demo / upload CSV)")
        uploaded = st.file_uploader("Upload CSV with columns: title, abstract, year, text (optional)", type="csv")
        if uploaded:
            df = pd.read_csv(uploaded)
            citations = df.to_dict(orient="records")
        else:
            # demo citations
            citations = [
                {"title": "Applying TransReact to Photocatalysis", "abstract":"We use TransReact and react-loss ...", "year":2023, "text": "We use TransReact and the react-loss introduced by ..."},
                {"title": "A Survey of reaction predictors", "abstract":"This survey discusses TransReact among others", "year":2024, "text": "TransReact ..."},
                {"title": "Transformer models in catalysis", "abstract":"No direct reuse", "year":2023, "text": "This paper mentions transformers but not TransReact specifically."}
            ]

        if st.button("Compute Concept Adoption"):
            with st.spinner("Extracting concepts and scanning citations..."):
                res = compute_concept_adoption(paper, citations)
            st.session_state["res"] = res
            st.success("Analysis complete")

    with col2:
        st.markdown("## Options")
        st.write("Semantic match threshold: 0.72 (tunable)")
        st.write("Embedding model: all-MiniLM-L6-v2")
        if st.button("Show candidate concepts"):
            candidates = build_candidate_concepts((paper["title"] + "\n\n" + paper["abstract"]))
            st.write("Top candidates:")
            for c in candidates[:40]:
                st.markdown(f"- {c}")

    # Display results elegantly
    if "res" in st.session_state:
        res = st.session_state["res"]
        # Top metric card
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([3,1,1])
        with c1:
            st.subheader(res["paper"]["title"])
            st.markdown(f"**DOI:** {res['paper'].get('doi','-')}")
            st.markdown(f"**Candidates extracted:** {res['n_candidates']}")
            st.markdown(f"**Citations analyzed:** {res['n_citations']}")
        with c2:
            st.metric("Concept Adoption Index", f"{res['cai']} / 100")
        with c3:
            # quick guidance
            st.markdown("**Interpretation**")
            st.write("• Higher CAI = concepts from the paper are more widely reused.")
        st.markdown("</div>", unsafe_allow_html=True)

        # Top concepts cards
        st.markdown("### 🔎 Top concepts (by reuse)")
        cols = st.columns(3)
        top = res["concepts"][:9]
        for i, c in enumerate(top):
            col = cols[i % 3]
            col.markdown(f"""
            <div class='card'>
            <div class='concept-title'>{c['concept']}</div>
            <div class='small-muted'>Total matches: {c['total_matches']} • Exact: {c['exact_count']} • Semantic: {c['semantic_count']}</div>
            <div style="margin-top:8px;">First reuse year: {c.get('first_year') or '—'}</div>
            <div style="margin-top:8px;font-size:0.95rem;color:#333">Velocity: {c['velocity']} matches/year</div>
            <details style="margin-top:8px"><summary>Matched documents ({len(c['matched_docs'])})</summary>
                <ul>
                {''.join([f"<li>{md['meta'].get('title','-')} ({md['meta'].get('year','-')}) — exact:{md['exact_matches']} sem:{int(md['semantic_match'])}</li>" for md in c['matched_docs']])}
                </ul>
            </details>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        # Adoption timeline
        st.markdown("### 📈 Adoption timeline")
        # build year counts per top concept
        all_years = []
        for c in res["concepts"]:
            for y in c.get("years", []):
                all_years.append(y)
        if all_years:
            year_counts = pd.Series(all_years).value_counts().sort_index()
            fig, ax = plt.subplots()
            ax.plot(year_counts.index, year_counts.values, marker='o')
            ax.set_xlabel("Year")
            ax.set_ylabel("Reuse count")
            ax.set_title("Concept reuse count over time (all concepts)")
            st.pyplot(fig)
        else:
            st.write("No reuse years found.")

        st.markdown("---")
        st.subheader("Component details JSON")
        st.json(res)

        # Download
        st.download_button("Download result JSON", json.dumps(res, indent=2), file_name="concept_adoption.json")

import streamlit as st
import matplotlib.pyplot as plt
from services import novelty_analysis
import json

def get_mock_input():
    return {
        "title": "Large Language Models for Predicting Catalyst Reaction Pathways",
        "abstract": "This work applies transformer-based models to simulate catalytic reaction pathways...",
        "keywords": ["catalysis", "transformer", "reaction prediction", "DFT replacement", "chemical AI"],
        "citation_count": 12,
        "publication_year": 2022,
        "field_baseline_citations": 48,
        "similarity_to_existing_work": 0.23,
        "paper_length_tokens": 4321,
        "num_references": 75,
        "num_figures": 12
    }

def get_mock_output():
    return {
        "classification": "Novel but Low-Cited",
        "score_breakdown": {
            "novelty_score": 0.84,
            "impact_score": 0.25
        },
        "explanation": "The paper introduces a new idea (transformers replacing DFT) in a domain where this is uncommon. Despite low citations (12 vs 48 field average), its high novelty score indicates originality. Time-lag may be a factor in citation delay."
    }


def render_novelty_card(input):

    data = json.loads(input) 
    # Custom CSS for card styling
    card_css = """
    <style>
    .card {
        background-color: #f9f9f9;
        border-left: 5px solid #1f77b4;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f77b4;
    }
    .score {
        font-size: 1.1rem;
        margin-top: 0.5rem;
        color: #333;
    }
    .explanation {
        font-size: 1rem;
        color: #555;
        margin-top: 1rem;
        line-height: 1.6;
    }
    </style>
    """

    # Inject CSS
    st.markdown(card_css, unsafe_allow_html=True)

    # Render the card
    st.markdown(f"""
    <div class="card">
        <div class="card-title">🧠 Classification: {data['classification']}</div>
        <div class="score">📊 Novelty Score: <b>{data['score_breakdown']['novelty_score']}</b></div>
        <div class="score">⭐ Impact Score: <b>{data['score_breakdown']['impact_score']}</b></div>
        <div class="explanation">💡 {data['explanation']}</div>
    </div>
    """, unsafe_allow_html=True)


def render_novelty_analysis(input: dict):
    # Simulate novelty
    similarity = novelty_analysis.simulate_similarity(input["abstract"])
    novelty, impact = novelty_analysis.compute_scores_v1(input["citation_count"], input["field_baseline_citations"], similarity)
    classification = novelty_analysis.classify_novelty_impact(input)

    # ---- Result Display ----
    st.subheader("📌 Classification Result")
    render_novelty_card(classification)

    #  st.markdown(f"**{classification}**")
    # st.write(f"**Novelty Score:** {novelty}")
    # st.write(f"**Impact Score:** {impact}")
    st.caption("Scores are scaled between 0 and 1")

    # ---- Plot ----
    st.subheader("🧠 Novelty vs Impact Map")

    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    ax.scatter(novelty, impact, color="red", s=50, edgecolors="black", label="Your Paper", zorder=5)

    # Background zones for visual guidance
    zones = {
        "Novel but Low-Cited": (0.7, 0.3),
        "Incremental but High-Cited": (0.3, 0.7),
        "Both Novel and High Impact": (0.8, 0.8),
        "Neither": (0.2, 0.2),
    }
    for label, (x, y) in zones.items():
        ax.scatter(x, y, color="gray", alpha=0.2, s=50, label=label)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Novelty Score", fontsize=6)
    ax.set_ylabel("Impact Score", fontsize=6)
    ax.grid(True)
    ax.legend(loc="lower right", fontsize=6)
    ax.set_title("Positioning of Your Paper", fontsize=6)
    ax.legend(fontsize=6)
    st.pyplot(fig)

            # Optional detailed explanation
    with st.expander("ℹ️ What does this mean?"):
        st.markdown("""
    - **Novelty Score** reflects how original your work is compared to existing literature (lower similarity → higher novelty).
    - **Impact Score** reflects citation performance relative to your field.
    - This helps detect underrecognized innovation or overhyped incremental work.
    """)

# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from services.bridging import compute_interdisciplinary_bridging, fetch_citations_with_fields
from services.llm_helpers import call_llm

def get_bridging_data_mock(paper_id, title=None):
    return  {
        "paper_id": "10.1000/exampledoi",
        "n_citations": 5,
        "field_counts": {
            "Computer Science": 3,
            "Genomics": 1,
            "Biology": 1,
            "Chemistry": 1,
            "Public Policy": 1
        },
        "components": {
            "breadth_entropy": 0.78,
            "mean_pairwise_distance": 0.42,
            "graph_betweenness": 0.05,
            "field_fraction_connected": 0.67
        },
        "weights": {"breadth":0.3,"distance":0.4,"betweenness":0.2,"field_fraction":0.1},
        "bridging_score": 57.84
     
    }

def explain_bridging_score_llm(bridging_data):
    """
    Generate a 2–3 sentence plain-text explanation of a paper's Interdisciplinary Bridging score.

    Args:
        bridging_data (dict): JSON-like dictionary containing bridging components and overall score.

    Returns:
        str: LLM-generated explanation (2-3 short sentences).
    """
    import json

    # Format the bridging data nicely for the LLM
    bridging_json = json.dumps(bridging_data, indent=2)

    # Build the LLM prompt
    prompt = f"""
You are an expert research-metrics communicator. 
Given this JSON with Interdisciplinary Bridging components and a bridging score, 
produce a concise 2–3 sentence summary that explains:
- whether the paper connects distant fields,
- which fields are most involved,
- what drove the bridging score (breadth, distance, or graph bridging),
- one short recommendation to increase bridging (if low).

Input:
{bridging_json}

Output: 2-3 short sentences in plain text.
    """
    return call_llm(prompt)

def normalize_fields_llm(raw_fields):
    """
    Normalize a list of raw field strings to canonical short, title-case labels.

    Args:
        raw_fields (list of str): List of raw field names from APIs.

    Returns:
        str: JSON string from LLM mapping raw field -> canonical field label.
    """
    # Join the raw fields into a bullet list for clarity in the prompt
    raw_list_str = "\n".join(f"- {field}" for field in raw_fields)

    # Build the LLM prompt
    prompt = f"""
You are a metadata normalizer. Given a list of raw field strings extracted from various APIs 
(e.g., "Comp Sci", "bioinformatics", "biol", "genomics", "health-policy"), map them to canonical 
field labels (short, title-case) and output JSON mapping raw -> canonical. Keep mappings consistent 
and suggest "Unknown" for empty or unrecognized inputs.

Input fields:
{raw_list_str}

Return JSON:
{{"raw_field": "Canonical Field", ...}}
    """
    return call_llm(prompt)

def render_bridging_ui():
    st.markdown("""
    <style>
    .card {background:#fff;padding:18px;border-radius:12px;box-shadow:0 8px 24px rgba(15,15,15,0.06);margin-bottom:14px;}
    .small {color:#666;font-size:0.95rem;}
    </style>
    """, unsafe_allow_html=True)
    # Input
    col1, col2 = st.columns([3,1])
    with col1:
        paper_id = st.text_input("Paper DOI or ID", value="10.1016/j.jfca.2025.107826")
        title = st.text_input("The effects of different patty positions and humidity levels on the quality and multiple hazards in roasted pork patties")
        if st.button("Compute Bridging Score"):
            with st.spinner("Fetching citations and computing bridging metrics..."):
                # In production fetch citations externally; here compute wrapper uses fetch stub
                citations = fetch_citations_with_fields(paper_id)
                res = compute_interdisciplinary_bridging(paper_id, paper_meta={"title":title}, citations=citations)
                st.session_state["bridging_res"] = res

    with col2:
        st.markdown("### Options")
        st.write("Field embedding model: all-MiniLM-L6-v2")
        st.write("Weights: breadth 30%, distance 40%, betweenness 20%, field_fraction 10%")

    # Results
    if "bridging_res" in st.session_state:
        res = st.session_state["bridging_res"]
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([3,1,1])
        with c1:
            st.subheader(res["paper_meta"].get("title", paper_id))
            st.markdown(f"**Paper ID:** {res['paper_id']}")
            st.markdown(f"**Citations analyzed:** {res['n_citations']}")
        with c2:
            st.metric(label="Interdisciplinary Bridging Score", value=f"{res['bridging_score']} / 100")
        with c3:
            st.markdown("**Top signals**")
            st.write(f"• Breadth (entropy): {res['components']['breadth_entropy']:.2f}")
            st.write(f"• Mean field distance: {res['components']['mean_pairwise_distance']:.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        # Field counts bar chart
        st.subheader("Field distribution among citing papers")
        fc = res["field_counts"]
        df = pd.DataFrame(list(fc.items()), columns=["field","count"]).sort_values("count", ascending=False)
        fig, ax = plt.subplots(figsize=(6,3))
        ax.barh(df["field"], df["count"])
        ax.set_xlabel("Citation count")
        ax.set_ylabel("")
        ax.invert_yaxis()
        st.pyplot(fig)

        st.markdown("---")
        # small network graph
        st.subheader("Paper → Citations → Fields (preview)")
        G = nx.Graph()
        paper_node = f"P:{res['paper_id']}"
        G.add_node(paper_node)
        for e in res["graph_edges"]:
            G.add_edge(e[0], e[1])
        # draw network (simple)
        pos = nx.spring_layout(G, seed=42, k=0.5)
        fig2, ax2 = plt.subplots(figsize=(6,4))
        node_colors = []
        sizes = []
        labels = {}
        for n,d in G.nodes(data=True):
            if isinstance(n, str) and n.startswith("P:"):
                node_colors.append("red"); sizes.append(400); labels[n] = "Paper"
            elif isinstance(n, str) and n.startswith("F:"):
                node_colors.append("#1f77b4"); sizes.append(300); labels[n] = n[2:]
            elif isinstance(n, str) and n.startswith("C:"):
                node_colors.append("#999999"); sizes.append(120); labels[n] = ""
            else:
                node_colors.append("#bbbbbb"); sizes.append(100); labels[n] = n
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=sizes, ax=ax2)
        nx.draw_networkx_edges(G, pos, alpha=0.5, ax=ax2)
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax2)
        ax2.axis("off")
        st.pyplot(fig2)

        st.markdown("---")
        st.subheader("Component details")
        st.json(res["components"])

        st.download_button("Download bridging result JSON", data=str(res), file_name="bridging_result.json", mime="application/json")



def test_normalize_fields_llm():
    """
    Test the normalize_fields_llm function with a sample input.
    """
    # Sample raw fields
    fields = ["Comp Sci", "bioinformatics", "biol", "genomics", "health-policy", ""]
    
    # Call the normalization function
    result_json = normalize_fields_llm(fields)
    
    # Print the result
    print(result_json)

def normalize_fields_llm_mock():
    return {
    "Comp Sci": "Computer Science",
    "bioinformatics": "Bioinformatics",
    "biol": "Biology",
    "genomics": "Genomics",
    "health-policy": "Health Policy",
    "": "Unknown"
    }

def test_explain_bridging_score_llm():
    """
    Test the explain_bridging_score_llm function with a sample bridging data.
    """
    # Sample bridging data
    bridging_data = {
        "paper_id": "10.1000/exampledoi",
        "n_citations": 5,
        "field_counts": {
            "Computer Science": 3,
            "Genomics": 1,
            "Biology": 1,
            "Chemistry": 1,
            "Public Policy": 1
        },
        "components": {
            "breadth_entropy": 0.78,
            "mean_pairwise_distance": 0.42,
            "graph_betweenness": 0.05,
            "field_fraction_connected": 0.67
        },
        "weights": {"breadth":0.3,"distance":0.4,"betweenness":0.2,"field_fraction":0.1},
        "bridging_score": 57.84
    }
    
    # Call the explanation function
    explanation = explain_bridging_score_llm(bridging_data)
    
    # Print the explanation
    print(explanation)


def test_compute_interdisciplinary_bridging():
    """
    Compute the interdisciplinary bridging score for a sample paper.
    """
    # Sample paper ID
    paper_id = "10.1000/exampledoi"
    
    # Call the compute function
    res = compute_interdisciplinary_bridging(paper_id)
    
    # Print the result
    print(res)

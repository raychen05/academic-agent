# citation_graph_influence.py
import networkx as nx
import numpy as np
from math import log
import pandas as pd
import streamlit as st
from components import  metric_card

def compute_topic_entropy(topic_counts):
    """Optional boost for topic diversity"""
    total = sum(topic_counts.values())
    probs = [v / total for v in topic_counts.values()]
    return -sum(p * log(p + 1e-10) for p in probs)

def citation_influence_score(graph: nx.DiGraph, paper_id: str, depth: int = 2):
    """
    Compute influence score for a paper by aggregating citations of citing papers (up to depth).
    - graph: Directed citation graph (cites → cited)
    - paper_id: DOI or internal paper ID
    - depth: How far downstream to explore
    """
    visited = set()
    influence_sum = 0.0
    topic_counts = {}

    def dfs(node, level):
        nonlocal influence_sum
        if level > depth or node in visited:
            return
        visited.add(node)

        # Get citing papers (i.e., papers that cite this node)
        citing_papers = [n for n in graph.predecessors(node)]
        for citing in citing_papers:
            metadata = graph.nodes[citing]
            citation_count = metadata.get("citation_count", 0)
            topic = metadata.get("topic", "unknown")

            edge_weight = 1 / (1 + level)  # decay with depth
            influence_sum += citation_count * edge_weight

            topic_counts[topic] = topic_counts.get(topic, 0) + 1

            dfs(citing, level + 1)

    dfs(paper_id, 0)

    topic_diversity_boost = 1 + compute_topic_entropy(topic_counts) / 3  # normalize entropy
    final_score = log(1 + influence_sum) * topic_diversity_boost

    return {
        "paper_id": paper_id,
        "raw_sum": influence_sum,
        "topic_entropy": compute_topic_entropy(topic_counts),
        "boosted_score": round(final_score, 3)
    }

def plot_citation_influence_score():
    G = nx.DiGraph()

    # Add papers and their metadata
    G.add_node("P1", citation_count=100, topic="AI")
    G.add_node("P2", citation_count=50, topic="AI")
    G.add_node("P3", citation_count=25, topic="Bio")
    G.add_node("P4", citation_count=10, topic="Physics")

    # Create citation edges (who cites whom)
    G.add_edge("P2", "P1")  # P2 cites P1
    G.add_edge("P3", "P1")  # P3 cites P1
    G.add_edge("P4", "P2")  # P4 cites P2

    score = citation_influence_score(G, paper_id="P1", depth=2)
    print(score)

    # Convert to DataFrame with one row
    #df = pd.DataFrame([score])

    # Display as table in Streamlit
    #st.dataframe(df, use_container_width=True)  # dynamic, scrollable
    # Or use st.table(df) for static table

    # Display as metrics in a row
    ''' 
    col0, col1, col2, col3 = st.columns(4)

    col0.metric("Paper ID", f"{score['paper_id']}")
    col1.metric("Raw Sum", f"{score['raw_sum']:.1f}")
    col2.metric("Topic Entropy", f"{score['topic_entropy']:.3f}")
    col3.metric("Boosted Score", f"{score['boosted_score']:.2f}")
    '''
    metric_card.render_metric_card(score)


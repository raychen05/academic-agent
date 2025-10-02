import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components

def render_topic_map(papers):
    st.subheader("📍 Topic Map")

    net = Network(height="600px", width="100%", notebook=False, directed=False)
    net.barnes_hut()

    cluster_colors = ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854"]

    for paper in papers:
        label = f"{paper['title']}"
        cluster = paper["cluster"]
        net.add_node(paper["id"], label=label, title=paper["abstract"], color=cluster_colors[cluster % len(cluster_colors)])

    # Add edges within clusters (optional)
    cluster_groups = {}
    for paper in papers:
        cluster_groups.setdefault(paper["cluster"], []).append(paper["id"])

    for group in cluster_groups.values():
        for i in range(len(group)):
            for j in range(i+1, len(group)):
                net.add_edge(group[i], group[j])

    net.show_buttons(filter_=['physics'])
    net.save_graph("topic_map.html")
    st.components.v1.html(open("topic_map.html", "r").read(), height=600, scrolling=True)

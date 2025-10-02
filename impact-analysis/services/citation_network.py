import networkx as nx
import matplotlib.pyplot as plt

def plot_network(author_name):
    G = nx.Graph()
    G.add_edges_from([
        ("Paper A", "Paper B"),
        ("Paper A", "Paper C"),
        ("Paper B", "Paper D")
    ])
    fig, ax = plt.subplots(figsize=(2, 1))
    nx.draw(
        G,
        with_labels=True,
        node_size=50,            # Size of the circle nodes
        node_color="#add8e6",      # Light blue fill
        font_size=3,              # Label font size
        font_color="black",
        edge_color="gray",
        width=0.2,  # <--- line width for edges
        ax=ax
    )
    return fig

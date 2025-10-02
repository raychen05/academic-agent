# tools/citation_graph.py
# This builds a simple citation graph using NetworkX — you can visualize it later with tools like PyVis or export to Neo4j.
# Build & query a citation network
# Load real graph from PubMed, CrossRef, or Neo4j


import networkx as nx

class CitationGraph:
    def __init__(self):
        """
        Example: Initialize an empty citation graph.
        Nodes = papers
        Edges = citations (A → B means A cites B)
        """
        self.graph = nx.DiGraph()

        # Dummy data
        self._load_dummy_data()

    def _load_dummy_data(self):
        """
        Load a sample citation network.
        """
        self.graph.add_node("Paper A", title="Transformer Models", year=2018)
        self.graph.add_node("Paper B", title="Attention is All You Need", year=2017)
        self.graph.add_node("Paper C", title="BERT: Pre-training", year=2019)

        self.graph.add_edge("Paper A", "Paper B")
        self.graph.add_edge("Paper C", "Paper B")
        self.graph.add_edge("Paper C", "Paper A")

    def get_cited_by(self, paper_id: str):
        """
        Return papers that cite the given paper.
        """
        return list(self.graph.predecessors(paper_id))

    def get_citations(self, paper_id: str):
        """
        Return papers that the given paper cites.
        """
        return list(self.graph.successors(paper_id))

    def find_key_nodes(self):
        """
        Find most cited papers (highest in-degree).
        """
        degrees = dict(self.graph.in_degree())
        sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        return sorted_nodes

    def visualize(self):
        """
        Optional: Export or draw with NetworkX.
        """
        import matplotlib.pyplot as plt
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', arrows=True)
        plt.show()
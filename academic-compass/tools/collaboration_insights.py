# collaboration_insights.py

from typing import List, Dict
import networkx as nx

class CollaborationInsights:
    """
    Builds a co-authorship network and provides collaboration suggestions.
    """

    def __init__(self, papers: List[Dict]):
        """
        Initialize with a list of papers.
        Each paper: { "title": str, "authors": List[str], "institution": str }
        """
        self.papers = papers
        self.graph = nx.Graph()
        self._build_network()

    def _build_network(self):
        """
        Build co-authorship network from papers.
        """
        for paper in self.papers:
            authors = paper.get("authors", [])
            for i in range(len(authors)):
                for j in range(i + 1, len(authors)):
                    self.graph.add_edge(authors[i], authors[j])

    def top_collaborators(self, researcher: str, top_n: int = 5) -> List[str]:
        """
        Get top collaborators for a researcher by connection strength (edge weight).
        """
        if researcher not in self.graph:
            return []

        neighbors = self.graph[researcher]
        sorted_neighbors = sorted(neighbors.items(), key=lambda x: x[1].get('weight', 1), reverse=True)
        return [name for name, _ in sorted_neighbors[:top_n]]

    def suggest_new_collaborators(self, researcher: str, top_n: int = 5) -> List[str]:
        """
        Suggest new collaborators using simple link prediction:
        find friends-of-friends not yet connected.
        """
        if researcher not in self.graph:
            return []

        neighbors = set(self.graph[researcher])
        foaf = set()
        for neighbor in neighbors:
            foaf.update(set(self.graph[neighbor]))
        foaf -= neighbors
        foaf.discard(researcher)

        # Rank by how many shared connections they have with the researcher
        suggestions = []
        for candidate in foaf:
            shared = neighbors.intersection(set(self.graph[candidate]))
            suggestions.append((candidate, len(shared)))

        suggestions.sort(key=lambda x: x[1], reverse=True)
        return [c[0] for c in suggestions[:top_n]]

    def institution_trends(self) -> Dict[str, int]:
        """
        Count how many papers each institution contributed to.
        """
        counts = {}
        for paper in self.papers:
            inst = paper.get("institution", "Unknown")
            counts[inst] = counts.get(inst, 0) + 1
        return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
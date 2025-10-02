# tests/test_citation_graph.py

import pytest
from tools.citation_graph import CitationGraph

def test_citation_graph_structure():
    graph = CitationGraph()
    assert "Paper B" in graph.graph
    cited_by = graph.get_cited_by("Paper B")
    assert isinstance(cited_by, list)
    assert len(graph.find_key_nodes()) > 0
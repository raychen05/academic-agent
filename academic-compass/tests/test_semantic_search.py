# tests/test_semantic_search.py

import pytest
from tools.semantic_search import SemanticSearch

def test_search_results():
    searcher = SemanticSearch()
    query = "How can AI help with climate change?"

    results = searcher.search(query, top_k=2)

    assert isinstance(results, list)
    assert len(results) == 2

    # Ensure at least one result is relevant
    relevant_found = any("Climate" in res["title"] for res in results)
    assert relevant_found, "Expected climate-related paper to appear"

    for res in results:
        assert "score" in res
        assert 0 <= res["score"] <= 1

# pytest tests/test_semantic_search.py -v
# tests/test_novelty.py
import pytest
from tools.novelty import NoveltyAnalyzer

def test_check_novelty():
    analyzer = NoveltyAnalyzer()
    result = analyzer.check_novelty("Transformers for Climate Modeling", ["Ref1", "Ref4"])

    assert 0 <= result["avg_embedding_similarity"] <= 1
    assert 0 <= result["citation_overlap_ratio"] <= 1
    assert 0 <= result["novelty_score"] <= 1
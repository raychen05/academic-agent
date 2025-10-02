# tests/test_grant_finder.py
import pytest
from tools.grant_finder import GrantFinder

def test_find_grants():
    finder = GrantFinder()
    grants = finder.find_grants("NLP")
    assert any("NLP" in str(g["matched_topics"]) for g in grants)
    assert all(g["relevance_score"] >= 0.5 for g in grants)

def test_suggest_high_priority_grants():
    finder = GrantFinder()
    grants = finder.suggest_high_priority_grants("NLP", min_score=0.7)
    assert all(g["relevance_score"] >= 0.7 for g in grants)
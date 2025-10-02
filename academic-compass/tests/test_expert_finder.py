# tests/test_expert_finder.py
import pytest
from tools.expert_finder import ExpertFinder

def test_find_experts():
    finder = ExpertFinder()
    experts = finder.find_experts("NLP")
    assert any("Alice Smith" in e["name"] for e in experts)
    assert all(e["relevance_score"] >= 0.5 for e in experts)

def test_suggest_reviewers():
    finder = ExpertFinder()
    reviewers = finder.suggest_reviewers("NLP")
    assert all(r["co_citation_score"] >= 0.7 for r in reviewers)
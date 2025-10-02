# test_collaboration_insights.py

import pytest
from tools.collaboration_insights import CollaborationInsights

@pytest.fixture
def sample_papers():
    return [
        {
            "title": "Paper A",
            "authors": ["Alice", "Bob", "Carol"],
            "institution": "University X"
        },
        {
            "title": "Paper B",
            "authors": ["Alice", "Dave"],
            "institution": "University X"
        },
        {
            "title": "Paper C",
            "authors": ["Eve", "Bob"],
            "institution": "Institute Y"
        },
        {
            "title": "Paper D",
            "authors": ["Frank", "Alice"],
            "institution": "University Z"
        }
    ]

def test_top_collaborators(sample_papers):
    ci = CollaborationInsights(sample_papers)
    top = ci.top_collaborators("Alice")
    assert "Bob" in top or "Dave" in top or "Frank" in top

def test_suggest_new_collaborators(sample_papers):
    ci = CollaborationInsights(sample_papers)
    suggestions = ci.suggest_new_collaborators("Alice")
    assert isinstance(suggestions, list)
    # Alice works with Bob, Bob works with Eve -> Eve could be suggested
    assert "Eve" in suggestions

def test_institution_trends(sample_papers):
    ci = CollaborationInsights(sample_papers)
    trends = ci.institution_trends()
    assert trends["University X"] == 2
    assert trends["Institute Y"] == 1
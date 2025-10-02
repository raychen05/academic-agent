import pytest
from tools.trend_detector import TrendDetector

def sample_records():
    return [
        {"year": 2020, "topic": "Topic A"},
        {"year": 2020, "topic": "Topic B"},
        {"year": 2021, "topic": "Topic A"},
        {"year": 2021, "topic": "Topic A"},
        {"year": 2022, "topic": "Topic A"},
        {"year": 2022, "topic": "Topic C"},
        {"year": 2023, "topic": "Topic C"},
        {"year": 2023, "topic": "Topic C"},
        {"year": 2023, "topic": "Topic C"},
    ]

def test_normalize_topics():
    td = TrendDetector()
    topics = [" Machine Learning ", "Deep Learning", "Graph  "]
    normalized = td.normalize_topics(topics)
    assert normalized == ["machine learning", "deep learning", "graph"]

def test_detect_trends():
    td = TrendDetector()
    trends = td.detect_trends(sample_records(), min_count=2)

    topics = trends["topic"].unique().tolist()
    assert "topic a" in topics
    assert "topic b" not in topics  # filtered out, only 1 count

def test_emerging_topics():
    td = TrendDetector()
    trends = td.detect_trends(sample_records(), min_count=1)
    emerging = td.emerging_topics(trends, recent_years=2, growth_threshold=0.2)

    assert "topic c" in emerging

def test_plot_trend(monkeypatch):
    import matplotlib.pyplot as plt
    td = TrendDetector()
    trends = td.detect_trends(sample_records())

    # Patch plt.show to prevent actual plot pop-up during test
    monkeypatch.setattr(plt, "show", lambda: None)
    td.plot_trend(trends, "Topic A")
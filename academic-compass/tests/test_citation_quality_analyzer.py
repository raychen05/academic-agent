# test_citation_quality_analyzer.py

import pytest
from tools.citation_quality_analyzer import CitationQualityAnalyzer

@pytest.fixture
def sample_contexts():
    return [
        "Smith et al. (2020) demonstrate a clear improvement over previous methods.",
        "However, as noted by Jones (2018), the proposed approach fails to scale.",
        "This technique, as described by Chen (2019), is commonly used in similar tasks."
    ]

def test_analyze_contexts(sample_contexts):
    analyzer = CitationQualityAnalyzer()
    results = analyzer.analyze_contexts(sample_contexts)

    assert isinstance(results, list)
    assert len(results) == len(sample_contexts)

    for result in results:
        assert result["label"] in ["supportive", "critical", "neutral"]
        assert 0 <= result["confidence"] <= 1

def test_summary_report(sample_contexts):
    analyzer = CitationQualityAnalyzer()
    report = analyzer.summary_report(sample_contexts)

    assert isinstance(report, dict)
    assert set(report.keys()) == {"supportive", "critical", "neutral"}
    assert sum(report.values()) == len(sample_contexts)
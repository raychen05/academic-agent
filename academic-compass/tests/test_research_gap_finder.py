# test_research_gap_finder.py

import pytest
from tools.research_gap_finder import ResearchGapFinder

@pytest.fixture
def sample_docs():
    return [
        "This paper investigates machine learning methods for medical imaging.",
        "We explore deep learning applications in cancer detection using X-ray data.",
        "A systematic review of neural networks for radiology image classification."
    ]

@pytest.fixture
def candidate_topics():
    return [
        "explainable AI in medical imaging",
        "transfer learning for rare diseases",
        "privacy-preserving data sharing",
        "multimodal learning",
        "edge computing for real-time diagnosis"
    ]

def test_keyphrase_extraction(sample_docs):
    gap_finder = ResearchGapFinder()
    phrases = gap_finder.extract_keyphrases(sample_docs)
    assert isinstance(phrases, list)
    assert len(phrases) > 0

def test_find_gaps(sample_docs, candidate_topics):
    gap_finder = ResearchGapFinder()
    gaps = gap_finder.find_research_gaps(sample_docs, candidate_topics)
    assert isinstance(gaps, list)
    assert all('topic' in g and 'coverage_score' in g for g in gaps)

def test_generate_gap_report(sample_docs, candidate_topics):
    gap_finder = ResearchGapFinder()
    report = gap_finder.generate_gap_report(sample_docs, candidate_topics)
    assert 'keyphrases' in report
    assert 'gap_analysis' in report
    assert isinstance(report['keyphrases'], list)
    assert isinstance(report['gap_analysis'], list)
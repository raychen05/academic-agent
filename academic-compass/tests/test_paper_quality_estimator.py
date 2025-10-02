# test_paper_quality_estimator.py

import pytest
from tools.paper_quality_estimator import PaperQualityEstimator

@pytest.fixture
def sample_retraction_list():
    return ["10.1234/retracted.5678"]

@pytest.fixture
def blacklisted_journals():
    return ["Fake Science Journal", "Predatory Open Access"]

@pytest.fixture
def sample_papers():
    return [
        {
            "doi": "10.1234/retracted.5678",
            "title": "A study that was retracted",
            "abstract": "This paper presents fake results on a topic.",
            "journal": "Good Journal",
            "citation_count": 2
        },
        {
            "doi": "10.5678/valid.1234",
            "title": "A solid paper",
            "abstract": "This is a robust study with valid results.",
            "journal": "Nature",
            "citation_count": 100
        },
        {
            "doi": "10.5678/shady.9999",
            "title": "Dubious research",
            "abstract": "A suspicious paper.",
            "journal": "Fake Science Journal",
            "citation_count": 0
        }
    ]

def test_check_retraction(sample_retraction_list):
    estimator = PaperQualityEstimator(retraction_list=sample_retraction_list)
    assert estimator.check_retraction("10.1234/retracted.5678") == True
    assert estimator.check_retraction("10.9999/nonretracted") == False

def test_basic_quality_checks(sample_papers, sample_retraction_list, blacklisted_journals):
    estimator = PaperQualityEstimator(
        retraction_list=sample_retraction_list,
        blacklisted_journals=blacklisted_journals
    )
    results = estimator.analyze_papers(sample_papers)
    assert isinstance(results, list)
    assert "quality_warnings" in results[0]

    retracted_paper = results[0]
    assert any("RETRACTED" in w for w in retracted_paper["quality_warnings"])

    blacklisted_paper = results[2]
    assert any("blacklisted journal" in w for w in blacklisted_paper["quality_warnings"])
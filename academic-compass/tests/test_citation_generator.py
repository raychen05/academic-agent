import pytest
from tools.citation_generator import CitationGenerator

@pytest.fixture
def sample_metadata():
    return {
        "authors": ["Jane Doe", "John Smith"],
        "title": "Deep Learning in Biomedical Research",
        "journal": "Journal of AI",
        "year": "2023",
        "volume": "12",
        "number": "3",
        "pages": "45-67",
        "doi": "10.1234/abcd.efgh"
    }

def test_generate_bibtex(sample_metadata):
    generator = CitationGenerator()
    bibtex = generator.generate_bibtex(sample_metadata)

    assert "@article" in bibtex
    assert "Jane Doe and John Smith" in bibtex
    assert "Deep Learning in Biomedical Research" in bibtex
    assert "Journal of AI" in bibtex

def test_generate_apa(sample_metadata):
    generator = CitationGenerator()
    apa = generator.generate_apa(sample_metadata)

    assert "Jane Doe, John Smith" in apa
    assert "Deep Learning in Biomedical Research" in apa
    assert "Journal of AI" in apa
    assert "(2023)" in apa

def test_generate_mla(sample_metadata):
    generator = CitationGenerator()
    mla = generator.generate_mla(sample_metadata)

    assert "Jane Doe, and John Smith." in mla
    assert "\"Deep Learning in Biomedical Research.\"" in mla
    assert "Journal of AI" in mla
    assert "vol. 12" in mla
    assert "no. 3" in mla
    assert "2023" in mla
    assert "pp. 45-67" in mla
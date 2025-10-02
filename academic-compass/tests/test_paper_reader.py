import pytest
from tools.paper_reader import PaperReader
import fitz  # PyMuPDF

@pytest.fixture
def sample_pdf(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "This is a test page about neural networks and gradient descent.")
    doc.save(pdf_path)
    doc.close()
    return pdf_path

def test_parse_pdf(sample_pdf):
    reader = PaperReader()
    sections = reader.parse_pdf(str(sample_pdf))

    assert isinstance(sections, list)
    assert len(sections) == 1
    assert "neural networks" in sections[0]["content"]

def test_extract_terms(sample_pdf):
    reader = PaperReader()
    sections = reader.parse_pdf(str(sample_pdf))

    glossary = ["neural network", "gradient descent", "transformer"]
    matches = reader.extract_terms(sections, glossary)

    assert "neural network" in matches
    assert "gradient descent" in matches
    assert "transformer" not in matches

def test_answer_question(sample_pdf):
    reader = PaperReader()
    sections = reader.parse_pdf(str(sample_pdf))

    question = "What is discussed about neural networks?"
    answer = reader.answer_question(question, sections)

    assert "Page 1" in answer
    assert "neural networks" in answer.lower()
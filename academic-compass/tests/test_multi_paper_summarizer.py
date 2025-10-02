# test_multi_paper_summarizer.py

import pytest
from tools.multi_paper_summarizer import MultiPaperSummarizer

@pytest.fixture
def sample_abstracts():
    return [
        "This paper presents a new method for image classification using deep convolutional neural networks.",
        "We explore the effects of data augmentation and transfer learning on medical image segmentation tasks.",
        "A systematic review of machine learning algorithms for natural language processing applications is conducted."
    ]

def test_summarize_papers_basic(sample_abstracts):
    summarizer = MultiPaperSummarizer()
    summary = summarizer.summarize_papers(sample_abstracts)
    assert isinstance(summary, str)
    assert len(summary) > 20  # Should produce some non-trivial output

def test_empty_input():
    summarizer = MultiPaperSummarizer()
    with pytest.raises(ValueError):
        summarizer.summarize_papers([])

def test_custom_length(sample_abstracts):
    summarizer = MultiPaperSummarizer()
    summary = summarizer.summarize_papers(sample_abstracts, max_length=50, min_length=20)
    assert isinstance(summary, str)
    assert len(summary.split()) <= 50
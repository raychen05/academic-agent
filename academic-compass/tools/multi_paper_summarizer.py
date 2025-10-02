# multi_paper_summarizer.py

from typing import List
from transformers import pipeline

class MultiPaperSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """
        Initialize summarizer with a transformer model.
        """
        self.summarizer = pipeline("summarization", model=model_name)

    def summarize_papers(self, abstracts: List[str], max_length: int = 200, min_length: int = 50) -> str:
        """
        Summarize multiple paper abstracts into a systematic review style summary.
        :param abstracts: List of paper abstracts (strings)
        :param max_length: Max length for the summary
        :param min_length: Min length for the summary
        :return: A single summary string
        """
        if not abstracts:
            raise ValueError("No abstracts provided.")

        # Combine all abstracts into one text blob
        combined_text = " ".join(abstracts)

        # Limit input length for models that can't handle very long input
        combined_text = combined_text[:3000]  # adjust as needed

        # Generate summary
        summary = self.summarizer(
            combined_text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )[0]['summary_text']

        return summary.strip()
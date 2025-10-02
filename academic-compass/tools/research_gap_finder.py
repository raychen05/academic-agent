# research_gap_finder.py

from typing import List, Dict
from keybert import KeyBERT
from transformers import pipeline

class ResearchGapFinder:
    def __init__(self, keybert_model: str = 'all-MiniLM-L6-v2', zero_shot_model: str = 'facebook/bart-large-mnli'):
        """
        Initialize keyphrase extractor and zero-shot classifier for finding gaps.
        """
        self.kw_model = KeyBERT(model=keybert_model)
        self.zero_shot = pipeline("zero-shot-classification", model=zero_shot_model)

    def extract_keyphrases(self, docs: List[str], top_n: int = 10) -> List[str]:
        """
        Extracts keyphrases across multiple docs.
        """
        text = " ".join(docs)
        keywords = self.kw_model.extract_keywords(text, top_n=top_n, stop_words='english')
        return [kw[0] for kw in keywords]

    def find_research_gaps(self, docs: List[str], candidate_gaps: List[str]) -> List[Dict[str, float]]:
        """
        Uses zero-shot classification to estimate how well candidate gaps are covered.
        Lower scores may indicate under-explored areas.
        """
        text = " ".join(docs)
        results = self.zero_shot(text, candidate_gaps)
        gaps = []
        for label, score in zip(results['labels'], results['scores']):
            gaps.append({
                "topic": label,
                "coverage_score": score,
                "gap_suggestion": f"Topic '{label}' may be under-explored." if score < 0.3 else f"Topic '{label}' seems well-covered."
            })
        return gaps

    def generate_gap_report(self, docs: List[str], candidate_gaps: List[str], top_n: int = 10) -> Dict:
        """
        Full gap report combining keyphrases + candidate gaps.
        """
        keyphrases = self.extract_keyphrases(docs, top_n)
        gap_scores = self.find_research_gaps(docs, candidate_gaps)
        return {
            "keyphrases": keyphrases,
            "gap_analysis": gap_scores
        }
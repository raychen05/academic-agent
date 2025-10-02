# citation_quality_analyzer.py

from typing import List, Dict
from transformers import pipeline

class CitationQualityAnalyzer:
    """
    Uses zero-shot classification to analyze citation contexts
    and classify each as 'supportive', 'critical', or 'neutral'.
    """

    def __init__(self, model_name: str = "facebook/bart-large-mnli"):
        self.classifier = pipeline("zero-shot-classification", model=model_name)

        # Define your citation stance labels
        self.labels = ["supportive", "critical", "neutral"]

    def analyze_contexts(self, contexts: List[str]) -> List[Dict[str, str]]:
        """
        Classify each citation context.
        :param contexts: List of text snippets containing citations
        :return: List of dicts with context, predicted label, and score
        """
        results = []
        for ctx in contexts:
            output = self.classifier(ctx, self.labels)
            predicted_label = output['labels'][0]
            score = output['scores'][0]
            results.append({
                "context": ctx,
                "label": predicted_label,
                "confidence": round(score, 3)
            })
        return results

    def summary_report(self, contexts: List[str]) -> Dict[str, int]:
        """
        Count how many citations fall into each category.
        """
        analysis = self.analyze_contexts(contexts)
        summary = {"supportive": 0, "critical": 0, "neutral": 0}
        for item in analysis:
            summary[item["label"]] += 1
        return summary
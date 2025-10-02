# tools/impact_eval.py
# Computes h-index, g-index, or normalized citation counts from dummy publication data.
# Calculate h-index, citations, altmetrics
# Pull real data from Scopus/Google Scholar API


from typing import List, Dict


class ImpactEvaluator:
    def __init__(self):
        """
        Example: Load dummy publications with citation counts & altmetrics.
        In production: link to Scopus, Google Scholar, OpenAlex, or Lens.org.
        """
        self.researcher_profile = {
            "name": "Dr. Alice Smith",
            "affiliation": "MIT",
            "publications": [
                {"title": "Paper A", "citations": 10, "altmetric_score": 50},
                {"title": "Paper B", "citations": 5, "altmetric_score": 20},
                {"title": "Paper C", "citations": 25, "altmetric_score": 80},
                {"title": "Paper D", "citations": 2, "altmetric_score": 5}
            ]
        }

    def compute_h_index(self):
        """
        Classic h-index calculation: max h where h papers have ≥ h citations.
        """
        citations = sorted([pub["citations"] for pub in self.researcher_profile["publications"]], reverse=True)
        h = 0
        for i, c in enumerate(citations, 1):
            if c >= i:
                h = i
            else:
                break
        return h

    def total_citations(self):
        """
        Sum of all citations.
        """
        return sum(pub["citations"] for pub in self.researcher_profile["publications"])

    def average_altmetric(self):
        """
        Simple average altmetric score.
        """
        scores = [pub["altmetric_score"] for pub in self.researcher_profile["publications"]]
        return sum(scores) / len(scores) if scores else 0

    def evaluate(self):
        """
        Return a compact researcher impact report.
        """
        return {
            "name": self.researcher_profile["name"],
            "affiliation": self.researcher_profile["affiliation"],
            "h_index": self.compute_h_index(),
            "total_citations": self.total_citations(),
            "average_altmetric": round(self.average_altmetric(), 2)
        }
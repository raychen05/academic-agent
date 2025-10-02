# tools/grant_finder.py
# Matches research queries to dummy grant calls — later you’d connect to NSF/NIH databases.

# tools/grant_finder.py

from datetime import datetime
import random

class GrantFinder:
    def __init__(self):
        """
        Example: In production, you'd connect to NSF, NIH, or Horizon Europe calls.
        """
        self.grants_db = [
            {
                "title": "NSF AI for Climate",
                "agency": "NSF",
                "topics": ["AI", "Climate Science", "Sustainability"],
                "description": "Funding AI research for climate adaptation and mitigation.",
                "deadline": "2025-09-01"
            },
            {
                "title": "NIH Genomics Research Grant",
                "agency": "NIH",
                "topics": ["Genomics", "Bioinformatics"],
                "description": "Supports cutting-edge genomic data science research.",
                "deadline": "2025-06-15"
            },
            {
                "title": "EU Horizon Quantum Computing",
                "agency": "EU Horizon",
                "topics": ["Quantum Computing", "Quantum Algorithms"],
                "description": "Research funding for next-gen quantum technologies.",
                "deadline": "2025-12-31"
            },
            {
                "title": "NSF NLP for Legal Studies",
                "agency": "NSF",
                "topics": ["NLP", "Legal Tech", "LLMs"],
                "description": "Funding NLP applications for improving legal text analysis.",
                "deadline": "2025-08-30"
            }
        ]

    def _is_future_deadline(self, date_str: str) -> bool:
        """
        Check if the grant deadline is still open.
        """
        deadline_date = datetime.strptime(date_str, "%Y-%m-%d")
        return deadline_date >= datetime.now()

    def find_grants(self, query_topic: str) -> list:
        """
        Match query topic/keywords to grants.
        Add a mock relevance score for ranking.
        """
        topic_lower = query_topic.lower()
        results = []

        for grant in self.grants_db:
            if not self._is_future_deadline(grant["deadline"]):
                continue

            matched_topics = [
                t for t in grant["topics"] if topic_lower in t.lower()
            ]
            if matched_topics:
                relevance_score = round(random.uniform(0.5, 1.0), 2)
                results.append({
                    "title": grant["title"],
                    "agency": grant["agency"],
                    "matched_topics": matched_topics,
                    "description": grant["description"],
                    "deadline": grant["deadline"],
                    "relevance_score": relevance_score
                })

        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results

    def suggest_high_priority_grants(self, query_topic: str, min_score: float = 0.7) -> list:
        """
        Return only grants with high relevance score.
        """
        matches = self.find_grants(query_topic)
        return [g for g in matches if g["relevance_score"] >= min_score]
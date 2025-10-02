# tools/expert_finder.py
# expert_finder.py — find top authors, reviewers, or collaborators
# Finds potential experts based on topic match or co-citation.
# This is a simple implementation that can be extended with a real database or API.
from typing import List, Dict
# tools/expert_finder.py

import random

class ExpertFinder:
    def __init__(self):
        """
        Example: Load dummy expert profiles.
        In production, connect to a graph DB (Neo4j) or citation index.
        """
        self.experts_db = [
            {
                "name": "Dr. Alice Smith",
                "affiliation": "MIT",
                "topics": ["NLP", "Large Language Models", "Text Summarization"],
                "co_citations": ["Paper A", "Paper B"]
            },
            {
                "name": "Prof. Bob Chen",
                "affiliation": "Stanford",
                "topics": ["Genomics", "Bioinformatics", "Protein Folding"],
                "co_citations": ["Paper C"]
            },
            {
                "name": "Dr. Maria Lopez",
                "affiliation": "Oxford",
                "topics": ["Climate Science", "Remote Sensing", "Earth Observation"],
                "co_citations": ["Paper D", "Paper E"]
            },
            {
                "name": "Dr. Yuki Tanaka",
                "affiliation": "University of Tokyo",
                "topics": ["Legal NLP", "Judicial Analysis", "LLMs"],
                "co_citations": ["Paper F"]
            }
        ]

    def find_experts(self, topic: str) -> list:
        """
        Return experts whose topics match the given query topic.
        Also add a mock co-citation score for ranking.
        """
        topic_lower = topic.lower()
        matches = []

        for expert in self.experts_db:
            matched_topics = [
                t for t in expert["topics"] if topic_lower in t.lower()
            ]
            if matched_topics:
                # Dummy co-citation score (in real life, count shared citations)
                co_citation_score = random.uniform(0.5, 1.0)
                matches.append({
                    "name": expert["name"],
                    "affiliation": expert["affiliation"],
                    "matched_topics": matched_topics,
                    "co_citation_score": round(co_citation_score, 2)
                })

        # Sort by co-citation score descending
        matches.sort(key=lambda x: x["co_citation_score"], reverse=True)
        return matches

    def suggest_reviewers(self, topic: str, min_score: float = 0.7) -> list:
        """
        Filter found experts for those with high co-citation score — suitable as reviewers.
        """
        experts = self.find_experts(topic)
        return [e for e in experts if e["co_citation_score"] >= min_score]
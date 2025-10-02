from services.llm_helpers import call_llm
from typing import List, Dict


def recommend_mock(author_name):
    return [
        "Submit to Nature Machine Intelligence.",
        "Co-author with researchers from MIT or ETH Zurich.",
        "Present at NeurIPS and CVPR."
    ]


def recommend_impact_strategy(
    title: str,
    abstract: str,
    keywords: List[str],
    author_affiliation: str,
    field: str
) -> Dict:
    prompt = f"""
You are a research impact strategist. Given a research paper, recommend a personalized plan for increasing its academic and real-world impact.

Your output should include:
1. Journals or venues to publish in (with justification)
2. Potential collaborators (with name, affiliation, and why they are relevant)
3. New research directions or topics to expand into
4. Dissemination strategies (e.g., public engagement, policy outreach, media)

Make recommendations specific to the content of the paper.

Title: {title}
Abstract: {abstract}
Keywords: {', '.join(keywords)}
Author Affiliation: {author_affiliation}
Field: {field}

Respond in the following JSON format:
{{
  "recommendations": {{
    "venues": [...],
    "collaborators": [...],
    "topics_to_expand": [...],
    "dissemination_strategies": [...]
  }}
}}
"""


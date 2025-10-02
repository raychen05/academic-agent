from services.llm_helpers import call_llm

from typing import List, Dict

def recommend_targets(title: str, abstract: str, keywords: List[str]) -> List[Dict]:
    prompt = f"""
You are an academic impact advisor. Given the metadata of a research paper, identify and recommend the top 3–5 target entities (e.g., policy bodies, funders, companies, journals, NGOs, or institutions) that are most likely to benefit from or help amplify the paper’s impact.

For each recommendation, provide:
1. Target name
2. Type (e.g., policy body, funder, journal, company, NGO)
3. A short, specific justification based on the paper’s content

Research Paper:
Title: {title}
Abstract: {abstract}
Keywords: {", ".join(keywords)}

Respond in JSON format:
[
  {{
    "target": "...",
    "type": "...",
    "justification": "..."
  }},
  ...
]
"""
    
    return call_llm(prompt)

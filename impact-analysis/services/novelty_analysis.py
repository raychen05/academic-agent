import random
from services.llm_helpers import call_llm
from typing import Dict

def simulate_similarity(text: str) -> float:
    # In production, replace with real semantic similarity calculation
    return round(random.uniform(0.2, 0.8), 2)

# --- Scoring and classification logic ---
def compute_scores_v1(citation_count, field_avg, similarity):
    novelty_score = 1 - similarity
    impact_score = citation_count / max(field_avg, 1)
    return round(novelty_score, 2), round(min(impact_score, 1.5), 2)  # clamp for scale


def compute_scores(input: dict) -> Dict:
    novelty_score = 1 - input.get("similarity_to_existing_work", 1.0)
    impact_score = input["citation_count"] / max(input["field_baseline_citations"], 1)

    return {
        "novelty_score": round(novelty_score, 2),
        "impact_score": round(impact_score, 2)
    }


def classify(novelty, impact):
    if novelty > 0.6 and impact < 0.4:
        return "🧪 Novel but Low-Cited"
    elif novelty < 0.4 and impact > 0.6:
        return "📈 Incremental but Highly-Cited"
    elif novelty > 0.6 and impact > 0.6:
        return "🏆 Both Novel and High Impact"
    else:
        return "⚠️ Neither"

def classify_novelty_impact(input: dict) -> dict:
    scores = compute_scores(input)

    prompt = f"""
You are a research metrics expert. A paper has been analyzed for novelty and impact using citation data and similarity scores.

Given the following metadata:
- Title: {input["title"]}
- Abstract: {input["abstract"]}
- Citation Count: {input["citation_count"]}
- Average Citation in Field: {input["field_baseline_citations"]}
- Novelty Score (0-1): {scores['novelty_score']}
- Impact Score (0-1): {scores['impact_score']}

Classify the paper into one of:
1. "Novel but Low-Cited"
2. "Incremental but Highly-Cited"
3. "Both Novel and High Impact"
4. "Neither Novel nor High Impact"

Then explain the reasoning briefly.

Respond in JSON format:
{{
  "classification": "...",
  "score_breakdown": {{
    "novelty_score": {scores['novelty_score']},
    "impact_score": {scores['impact_score']}
  }},
  "explanation": "..."
}}
"""
    return call_llm(prompt)

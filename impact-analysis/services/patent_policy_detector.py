from services.llm_helpers import call_llm
from sentence_transformers import SentenceTransformer, util
import requests


def detect_policy_patent_impact_mock():
    # Simulate downstream mentions
    return {
        "impact_detected": True,
        "sources": [
            {
            "type": "patent",
            "title": "System and method for neural network-based quantum simulations",
            "url": "https://patents.google.com/patent/US2024032193A1",
            "score": 0.95
            },
            {
            "type": "policy",
            "title": "US DOE Strategic Plan on AI in Science",
            "url": "https://energy.gov/ai-plan",
            "score": 0.90
            }
        ],
        "llm_explanation": "The paper has been referenced in a patent filed by XYZ Corp and a U.S. Department of Energy strategic document. This indicates its influence in both commercial innovation and government policy."
    }

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text):
    return model.encode(text, convert_to_tensor=True)

def match_sources(paper_text, candidate_sources, threshold=0.75):
    paper_vec = embed(paper_text)
    matches = []

    for source in candidate_sources:
        score = util.cos_sim(paper_vec, embed(source["text"])).item()
        if score > threshold:
            source["score"] = score
            matches.append(source)

    return sorted(matches, key=lambda x: -x["score"])


def detect_policy_patent_impact(title, abstract, sources):
    paper_text = f"{title}\n\n{abstract}"
    matched = match_sources(paper_text, sources)

    result = {
        "impact_detected": len(matched) > 0,
        "sources": matched,
    }

    return result

def detect_with_llm_explanation(title, abstract):
    raw_result = detect_policy_patent_impact(title, abstract)
    if raw_result["impact_detected"]:
        raw_result["llm_explanation"] = explain_impact_with_llm(
            title, abstract, raw_result["sources"]
        )
    return raw_result

def explain_impact_with_llm(title, abstract, matches):
    context = "\n".join([f"{m['type'].title()}: {m['title']} - {m['url']}" for m in matches])
    
    prompt = f"""
You are an expert in science communication and impact analysis.
Given the paper:

Title: {title}

Abstract: {abstract}

And the following matched real-world citations:
{context}

Explain in 2-3 sentences how these matches indicate real-world impact (e.g., cited in patent or government policy).
"""

    return call_llm(prompt)



def detect_with_llm_explanation(title, abstract):
    raw_result = detect_policy_patent_impact_mock()
    if raw_result["impact_detected"]:
        raw_result["llm_explanation"] = explain_impact_with_llm(
            title, abstract, raw_result["sources"]
        )
    return raw_result
from langchain.tools import tool
from utils.similarity import compute_semantic_similarity
from utils.embedding import get_keywords_tfidf

@tool
def analyze_novelty(abstract: str, related_abstracts: list) -> str:
    """Compare abstract against related ones to evaluate novelty."""
    sim_score = compute_semantic_similarity(abstract, related_abstracts)
    new_keywords = get_keywords_tfidf(abstract, related_abstracts)

    return f"Novelty Score: {1-sim_score:.2f}\nUnique keywords: {', '.join(new_keywords[:5])}"

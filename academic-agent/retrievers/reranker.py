# reranker.py
from typing import List, Tuple

class Reranker:
    """
    Example reranker that scores retrieved documents based on relevance.
    """

    def __init__(self, model=None):
        """
        model: could be a cross-encoder or any model that can score (query, doc) pairs.
        """
        self.model = model  # Plug in your cross-encoder if you have one

    def rerank(self, query: str, docs: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        """
        docs: list of (doc_text, initial_score)
        returns: list of (doc_text, reranked_score)
        """
        # Placeholder: Boost score for presence of query terms
        reranked = []
        for doc_text, init_score in docs:
            relevance_boost = sum([1 for word in query.lower().split() if word in doc_text.lower()])
            final_score = init_score + relevance_boost
            reranked.append((doc_text, final_score))

        reranked.sort(key=lambda x: x[1], reverse=True)
        return reranked
import math
from typing import List, Dict

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

def vector_search_tool(query_vector: List[float], documents: List[Dict]) -> List[Dict]:
    """
    Search documents by comparing their vector representations with the query vector.
    Returns documents sorted by similarity score in descending order.

    Args:
        query_vector: List of floats representing the query vector.
        documents: List of dicts, each with at least a 'vector' key (list of floats) and other metadata.

    Returns:
        List of documents with an added 'similarity' key, sorted by similarity descending.
    """
    results = []
    for doc in documents:
        sim = cosine_similarity(query_vector, doc['vector'])
        doc_with_score = doc.copy()
        doc_with_score['similarity'] = sim
        results.append(doc_with_score)

    # Sort by similarity descending
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results

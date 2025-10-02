from rapidfuzz import fuzz

def fuzzy_rerank(query, candidates, limit=3):
    return sorted(
        candidates,
        key=lambda x: fuzz.token_sort_ratio(query, x[0]),
        reverse=True
    )[:limit]

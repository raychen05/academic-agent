from rapidfuzz import process, fuzz

def fuzzy_topk(query: str, choices: list[str], k=20):
    return process.extract(query, choices, limit=k, scorer=fuzz.token_sort_ratio)

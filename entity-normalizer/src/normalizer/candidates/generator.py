# src/normalizer/candidates/generator.py
from rapidfuzz import process, fuzz

def gen_fuzzy(name: str, names: list[str], k=20):
    return process.extract(name, names, limit=k, scorer=fuzz.token_sort_ratio)

def gen_candidates(name: str, names: list[str], faiss_searcher: FaissSearcher, k_embed=50, k_fuzzy=20):
    fuzzy = gen_fuzzy(name, names, k=k_fuzzy)  # [(candidate, score0..100), ...]
    embed = [(names[i], s) for i, s in faiss_searcher.search(name, k=k_embed)]
    # de-duplicate by best score
    bag = {}
    for cand, s in fuzzy:
        bag[cand] = max(bag.get(cand, 0), 0.5 * (s/100))
    for cand, s in embed:
        bag[cand] = max(bag.get(cand, 0), bag.get(cand, 0) + 0.5 * s)
    return sorted(bag.items(), key=lambda x: x[1], reverse=True)

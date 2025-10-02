# src/normalizer/ranking/reranker.py
from rapidfuzz import fuzz

def hybrid_score(user_input: str, cand_name: str, embed_score: float, entity_weights: dict) -> float:
    fuzzy = fuzz.token_sort_ratio(user_input, cand_name) / 100.0
    α, β = entity_weights["alpha_fuzzy"], entity_weights["beta_embed"]
    return α * fuzzy + β * embed_score

def final_score(user_input, cand_name, embed_score, ctx_s, entity_weights):
    base = hybrid_score(user_input, cand_name, embed_score, entity_weights)
    γ = entity_weights["gamma_ctx"]
    return base + γ * ctx_s

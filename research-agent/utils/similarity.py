
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_semantic_similarity(text: str, others: list) -> float:
    embeddings = model.encode([text] + others)
    query_vec = embeddings[0].reshape(1, -1)
    corpus_vecs = embeddings[1:]
    sims = cosine_similarity(query_vec, corpus_vecs)
    return float(np.mean(sims))
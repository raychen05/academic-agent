
from sentence_transformers import SentenceTransformer

_model = None

def get_embedder(model_name="all-MiniLM-L6-v2"):
    global _model
    if _model is None:
        _model = SentenceTransformer(model_name)
    return _model

def encode(texts):
    model = get_embedder()
    return model.encode(texts, normalize_embeddings=True)


# src/normalizer/candidates/faiss_index.py
import faiss, numpy as np
from sentence_transformers import SentenceTransformer

class FaissSearcher:
    def __init__(self, names, model_name, index_path=None, normalize=True):
        self.names = names
        self.model = SentenceTransformer(model_name)
        self.normalize = normalize
        if index_path and Path(index_path).exists():
            self.index = faiss.read_index(str(index_path))
            self.embeds = np.load(str(Path(index_path).with_suffix(".ids.npy")))
        else:
            X = self.model.encode(names, normalize_embeddings=True)
            self.index = faiss.IndexFlatIP(X.shape[1])
            self.index.add(X)
            self.embeds = X  # keep in memory for serialization

    def search(self, query: str, k=50):
        q = self.model.encode([query], normalize_embeddings=True)
        D, I = self.index.search(q, k)
        return [(int(i), float(s)) for i, s in zip(I[0], D[0])]


# Top-k vector match with FAISS

import numpy as np
import faiss
import json
from matching.embedder import NameEmbedder

class FAISSNameMatcher:
    def __init__(self, index_path: str, name_list_path: str):
        self.names = json.load(open(name_list_path))
        self.embeddings = np.load(index_path)
        self.embedder = NameEmbedder()

        # Init FAISS index
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)

    def match(self, query_name: str, k=5):
        query_vec = np.array(self.embedder.embed(query_name)).reshape(1, -1)
        D, I = self.index.search(query_vec, k)

        results = []
        for i, score in zip(I[0], D[0]):
            results.append({"name": self.names[i], "score": float(score)})

        return results

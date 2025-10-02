import faiss
import numpy as np
import pandas as pd
from .embed import encode

class OrgVectorIndex:
    def __init__(self):
        self.names = []
        self.index = None

    def build(self, name_list):
        self.names = name_list
        embeddings = encode(name_list)
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings.astype('float32'))

    def search(self, query: str, top_k=5):
        query_vec = encode([query])
        D, I = self.index.search(query_vec.astype('float32'), top_k)
        return [(self.names[i], float(D[0][j])) for j, i in enumerate(I[0])]


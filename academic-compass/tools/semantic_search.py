# tools/semantic_search.py
# functional version with FAISS


import numpy as np
from sentence_transformers import SentenceTransformer

class SemanticSearch:
    def __init__(self):
        self.memory_manager = memory_manager
        # Example papers — you can load from DB instead.
        self.papers = [
            {"id": 1, "title": "Deep Learning for NLP", "abstract": "Explores LSTM and Transformer models."},
            {"id": 2, "title": "Quantum Computing Basics", "abstract": "Introduces qubits and entanglement."},
            {"id": 3, "title": "Climate Modeling with AI", "abstract": "Applies ML models to climate predictions."}
        ]

        self.model = SentenceTransformer("all-MiniLM-L6-v2")  # small and fast

        self.embeddings = self._embed_papers()
        self.index = self._build_faiss_index()

    

    def embed_query(self, query):
        """
        Example: call OpenAI Embeddings or mock.
        """
        return [0.1] * 1536

    def _embed_papers(self):
        texts = [paper["title"] + " " + paper["abstract"] for paper in self.papers]
        embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings

    def _build_faiss_index(self):
        dim = self.embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)  # Inner Product for cosine similarity if normalized
        index.add(self.embeddings)
        return index

    def search(self, query, top_k=2):
        query_embedding = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            paper = self.papers[idx]
            results.append({
                "id": paper["id"],
                "title": paper["title"],
                "score": round(float(score), 3)
            })
        return results
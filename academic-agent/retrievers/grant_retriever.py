# grant_retriever.py

from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class GrantRetriever:
    """
    Uses SentenceTransformers + FAISS to retrieve similar grants.
    """

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Example knowledge base of grant docs
        self.knowledge_base = [
            "Grant A: Funding for AI-driven healthcare diagnostic tools, with focus on imaging and predictive analytics.",
            "Grant B: EU Horizon 2020 project supporting machine learning for climate adaptation in coastal regions.",
            "Grant C: National Science Foundation grant for renewable energy storage innovations.",
            "Grant D: Bill & Melinda Gates Foundation supporting AI for sustainability and agriculture.",
            "Grant E: US Department of Energy funding for quantum computing breakthroughs in materials science.",
            "Grant F: UK Research and Innovation grant for quantum applications in new battery materials.",
            "Grant G: European Research Council funding for AI-based climate risk models and data-driven policy."
        ]

        self.embeddings = self.model.encode(self.knowledge_base, convert_to_numpy=True)
        self.dimension = self.embeddings.shape[1]

        # Create FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(self.embeddings)
        print(f"[GrantRetriever] FAISS index initialized with {len(self.knowledge_base)} documents.")

    def retrieve(self, query: str) -> List[Tuple[str, float]]:
        """
        Retrieve top-k similar docs.
        """
        query_emb = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_emb, k=3)

        results = []
        for idx, score in zip(I[0], D[0]):
            results.append((self.knowledge_base[idx], -score))  # Negative L2 distance as similarity

        print(f"[GrantRetriever] Retrieved top docs for query: '{query}'")
        return results
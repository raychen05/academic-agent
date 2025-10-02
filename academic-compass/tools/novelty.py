# tools/novelty.py
#T his checks a topic’s novelty using:
#	1.	Embedding similarity — compare topic embedding to similar past works.
#	2.	Citation overlap — more overlap = less novelty.
# Combines embedding similarity + citation overlap
# Use real vector DB (e.g., Pinecone) + reference parser



import numpy as np


class NoveltyAnalyzer:
    def __init__(self):
        # Dummy prior embeddings (e.g., similar papers)
        self.prior_embeddings = [
            np.array([0.1] * 1536),
            np.array([0.2] * 1536)
        ]

        # Dummy citation overlap database
        self.prior_citations = [
            {"title": "Paper A", "citations": ["Ref1", "Ref2", "Ref3"]},
            {"title": "Paper B", "citations": ["Ref2", "Ref3"]}
        ]

    def embed_topic(self, topic: str):
        """
        Example: Use OpenAI or other embeddings API.
        """
        return np.array([0.15] * 1536)

    def cosine_similarity(self, vec1, vec2):
        """
        Compute cosine similarity between two vectors.
        """
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def check_novelty(self, topic: str, cited_refs: list):
        """
        Estimate novelty score: lower similarity & fewer overlapping citations → higher novelty.
        """
        topic_embedding = self.embed_topic(topic)

        similarities = [self.cosine_similarity(topic_embedding, emb) for emb in self.prior_embeddings]
        avg_sim = sum(similarities) / len(similarities)

        all_prior_refs = set()
        for prior in self.prior_citations:
            all_prior_refs.update(prior["citations"])

        overlap = len(set(cited_refs) & all_prior_refs)
        overlap_ratio = overlap / len(cited_refs) if cited_refs else 0

        # Simple novelty score: lower is more novel
        novelty_score = (avg_sim + overlap_ratio) / 2

        return {
            "avg_embedding_similarity": avg_sim,
            "citation_overlap_ratio": overlap_ratio,
            "novelty_score": novelty_score
        }
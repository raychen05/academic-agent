from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("allenai-specter")

def build_author_profile(papers):
    # Average embeddings of papers written by an author
    vectors = []
    for paper in papers:
        vec = model.encode(paper["title"] + " " + paper.get("abstract", ""), convert_to_numpy=True)
        vectors.append(vec)
    return np.mean(vectors, axis=0)

def compare_authors(author1_vec, author2_vec):
    dot = np.dot(author1_vec, author2_vec)
    norm = np.linalg.norm(author1_vec) * np.linalg.norm(author2_vec)
    return dot / norm

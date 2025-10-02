from sentence_transformers import SentenceTransformer, util
import numpy as np
import faiss
import pickle



# model = SentenceTransformer('allenai-specter')  # Optimized for academic papers
model = SentenceTransformer("all-MiniLM-L6-v2")  # fast and lightweight

def encode_text(text):
    return model.encode(text, convert_to_tensor=True)

def semantic_rank(query, papers):
    query_vec = encode_text(query)
    results = []
    for paper in papers:
        paper_vec = encode_text(paper["title"] + " " + paper["abstract"])
        score = float(util.cos_sim(query_vec, paper_vec)[0])
        results.append((score, paper))
    return sorted(results, reverse=True, key=lambda x: x[0])


def build_faiss_index(papers):
    texts = [p["title"] + ". " + p["abstract"] for p in papers]
    embeddings = model.encode(texts, convert_to_tensor=False)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
    with open("index.pkl", "wb") as f:
        pickle.dump((index, papers), f)


def load_index():
    with open("index.pkl", "rb") as f:
        index, papers = pickle.load(f)
    return index, papers

def retrieve(query, k=5):
    index, papers = load_index()
    query_embedding = model.encode([query])[0]
    distances, indices = index.search(np.array([query_embedding]), k)
    return [papers[i] for i in indices[0]]

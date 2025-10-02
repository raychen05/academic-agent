from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from pyvis.network import Network
import streamlit as st
import pandas as pd

# Sample paper data
papers = [
    {"id": "p1", "title": "GAN for pathology", "abstract": "We use GANs to segment medical images"},
    {"id": "p2", "title": "Transformers for drugs", "abstract": "Transformers help predict molecules"},
    {"id": "p3", "title": "Graph neural nets for proteins", "abstract": "Use GNNs to model protein structure"},
    {"id": "p4", "title": "CycleGAN in radiology", "abstract": "CycleGAN for image style translation"},
    {"id": "p5", "title": "LLMs in medical Q&A", "abstract": "LLMs answer patient questions"},
]

# Embed and cluster
def cluster_papers(papers, n_clusters=3):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [p["title"] + ". " + p["abstract"] for p in papers]
    embeddings = model.encode(texts)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    # Add cluster labels
    for i, paper in enumerate(papers):
        paper["cluster"] = int(labels[i])
    
    return papers

clustered_papers = cluster_papers(papers)
print(clustered_papers)



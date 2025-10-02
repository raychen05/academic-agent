from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from typing import List
from config import settings
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(settings.EMBEDDING_MODEL)
client = QdrantClient(url=settings.QDRANT_URL)
COLLECTION = "memories"

# ensure collection exists
if COLLECTION not in [c.name for c in client.get_collections().collections]:
    client.recreate_collection(collection_name=COLLECTION, vectors_config={"size": model.get_sentence_embedding_dimension(), "distance": "Cosine"})

def embed_text(texts: List[str]):
    return model.encode(texts, convert_to_numpy=True)

def upsert_memories(items: List[dict]):
    # items: [{"id": str, "text": str, "meta": {...}}]
    texts = [it['text'] for it in items]
    vectors = embed_text(texts)
    payload = [it['meta'] for it in items]
    ids = [it['id'] for it in items]
    client.upsert(collection_name=COLLECTION, points=[{"id": id_, "vector": vec.tolist(), "payload": p} for id_, vec, p in zip(ids, vectors, payload)])

def search(query: str, top_k: int = 5):
    qv = embed_text([query])[0].tolist()
    res = client.search(collection_name=COLLECTION, query_vector=qv, limit=top_k)
    return res
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams
import os
from dotenv import load_dotenv

load_dotenv()
qdrant_url = os.getenv("QDRANT_URL")
client = QdrantClient(url=qdrant_url)

collection_name = "summaries"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=1536, distance="Cosine"),
)
print(f"Collection '{collection_name}' initialized.")
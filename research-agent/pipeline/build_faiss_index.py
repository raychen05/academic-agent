
# Builds a FAISS index from documents.

# retrievers/build_faiss_index.py

import json
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from config import VECTOR_INDEX_PATH, DOCS_PATH

def build_faiss_index():
    with open(DOCS_PATH, "r") as f:
        docs_raw = json.load(f)
    
    documents = [
        Document(
            page_content=doc["abstract"] or doc["content"],
            metadata={"title": doc["title"], "source": doc["source"], "year": doc["year"]}
        )
        for doc in docs_raw
    ]
    
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(documents, embeddings)
    db.save_local(VECTOR_INDEX_PATH)
    print(f"FAISS index saved to {VECTOR_INDEX_PATH}")

if __name__ == "__main__":
    build_faiss_index()


#Loads a BM25 retriever from the same documents.

# retrievers/load_bm25_retriever.py

import json
from langchain.retrievers import BM25Retriever
from langchain.schema import Document
from config import DOCS_PATH

def load_bm25_retriever():
    with open(DOCS_PATH, "r") as f:
        docs_raw = json.load(f)

    documents = [
        Document(
            page_content=doc["abstract"] or doc["content"],
            metadata={"title": doc["title"], "source": doc["source"], "year": doc["year"]}
        )
        for doc in docs_raw
    ]
    
    retriever = BM25Retriever.from_documents(documents)
    retriever.k = 5
    return retriever

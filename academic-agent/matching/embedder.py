 
# Use OpenAI or HuggingFace model

from openai import OpenAIEmbeddings  # Or use SentenceTransformer from transformers

class NameEmbedder:
    def __init__(self, model="text-embedding-3-small"):
        self.embedder = OpenAIEmbeddings(model=model)

    def embed(self, name: str):
        return self.embedder.embed_query(name)

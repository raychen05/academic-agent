
# Precomputing Embeddings (prepare_faiss_index.py)

import json
import numpy as np
from matching.embedder import NameEmbedder

names = json.load(open("data/author_names.json"))
embedder = NameEmbedder()

embeddings = [embedder.embed(name) for name in names]
np.save("data/author_embeddings.npy", np.array(embeddings))

# src/normalizer/config.py
from pathlib import Path
import yaml

class AppConfig:
    def __init__(self, cfg_path: str = "configs/app.yaml"):
        d = yaml.safe_load(open(cfg_path))
        self.model_name = d["embeddings"]["model_name"]       # "BAAI/bge-small-en"
        self.index_path = Path(d["embeddings"]["index_path"]) # "data/embeddings/indexes/journals.faiss"
        self.use_qdrant = d.get("qdrant", {}).get("enabled", False)
        self.cache = d.get("cache", {"enabled": False})
        self.weights = yaml.safe_load(open("configs/weights.yaml"))

CFG = AppConfig()

# long_term.py

import os
import json

class LongTermMemory:
    """
    Example long-term memory using local JSON.
    Replace with a vector DB or database for production.
    """

    def __init__(self, storage_file="long_term_memory.json"):
        self.storage_file = storage_file
        self.memory = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                return json.load(f)
        else:
            return {}

    def store(self, key: str, data: dict):
        self.memory[key] = data
        with open(self.storage_file, "w") as f:
            json.dump(self.memory, f)
        print(f"[LongTermMemory] Stored: {key}")

    def retrieve(self, key: str):
        return self.memory.get(key, None)

    def all(self):
        return self.memory
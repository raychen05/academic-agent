# agent/memory.py
# Stores + loads FAISS index
#Stores feedback in SQLite

import faiss
import numpy as np
import os
import sqlite3

class MemoryManager:
    def __init__(self, index_path="data/memory_index/index.faiss", db_path="data/memory_index/feedback.db"):
        self.index_path = index_path
        self.db_path = db_path

        self.dim = 1536  # Example for OpenAI embeddings
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            print("✅ Loaded existing FAISS index.")
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            print("✅ Created new FAISS index.")

        self.metadata = []  # Store text alongside vector IDs

        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._create_feedback_table()

    def add_to_index(self, text, embedding):
        vec = np.array(embedding).astype('float32').reshape(1, -1)
        self.index.add(vec)
        self.metadata.append(text)

    def search_index(self, embedding, k=3):
        vec = np.array(embedding).astype('float32').reshape(1, -1)
        D, I = self.index.search(vec, k)
        results = []
        for idx in I[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results

    def save_index(self):
        faiss.write_index(self.index, self.index_path)
        print(f"✅ FAISS index saved to {self.index_path}")

    def _create_feedback_table(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                answer TEXT,
                feedback TEXT,
                self_eval_score REAL
            )
        """)
        self.conn.commit()

    def store_feedback(self, query, answer, feedback, score):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO feedback (query, answer, feedback, self_eval_score)
            VALUES (?, ?, ?, ?)
        """, (query, answer, feedback, score))
        self.conn.commit()
        print("✅ Feedback stored in SQLite.")
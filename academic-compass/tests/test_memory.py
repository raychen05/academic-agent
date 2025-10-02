# tests/test_memory_manager.py

import os
import faiss-gpu
import numpy as np
import sqlite3
import pytest

from agent.memory import MemoryManager

@pytest.fixture
def memory_manager(tmp_path):
    index_path = tmp_path / "index.faiss"
    db_path = tmp_path / "feedback.db"
    mm = MemoryManager(str(index_path), str(db_path))
    yield mm
    # Cleanup connections if needed
    mm.conn.close()

def test_faiss_index_creation(memory_manager):
    # New index should be empty
    assert memory_manager.index.ntotal == 0
    assert memory_manager.metadata == []

def test_add_and_search_index(memory_manager):
    text = "Sample document text"
    embedding = np.random.rand(memory_manager.dim).astype('float32')

    memory_manager.add_to_index(text, embedding)

    assert memory_manager.index.ntotal == 1
    assert memory_manager.metadata[0] == text

    results = memory_manager.search_index(embedding, k=1)
    assert len(results) == 1
    assert results[0] == text

def test_save_and_load_index(tmp_path):
    index_path = tmp_path / "index.faiss"
    db_path = tmp_path / "feedback.db"

    mm = MemoryManager(str(index_path), str(db_path))

    text = "Persisted text"
    embedding = np.random.rand(mm.dim).astype('float32')
    mm.add_to_index(text, embedding)

    mm.save_index()
    assert os.path.exists(index_path)

    # Load a new instance and verify index loads correctly
    mm2 = MemoryManager(str(index_path), str(db_path))
    assert mm2.index.ntotal == 1
    results = mm2.search_index(embedding, k=1)
    assert results[0] == text

    mm.conn.close()
    mm2.conn.close()

def test_store_feedback_and_db_query(memory_manager):
    query = "What is AI?"
    answer = "AI stands for Artificial Intelligence."
    feedback = "5"
    score = 4.5

    memory_manager.store_feedback(query, answer, feedback, score)

    # Query back the feedback table directly
    cur = memory_manager.conn.cursor()
    cur.execute("SELECT query, answer, feedback, self_eval_score FROM feedback WHERE query=?", (query,))
    row = cur.fetchone()

    assert row is not None
    assert row[0] == query
    assert row[1] == answer
    assert row[2] == feedback
    assert abs(row[3] - score) < 1e-6  # floating point comparison

    memory_manager.conn.close()


    # pytest tests/test_memory_manager.py -v
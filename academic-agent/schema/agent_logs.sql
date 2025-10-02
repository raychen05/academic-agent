CREATE TABLE agent_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    query TEXT,
    retrieved_docs JSONB,
    reranked_docs JSONB,
    summary TEXT,
    self_eval_score FLOAT,
    feedback TEXT,
    feedback_score FLOAT,
    episodic_memory JSONB
);
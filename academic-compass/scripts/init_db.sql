-- init_db.sql

-- create agent_logs table，Store all conversations and self-learning data.
CREATE TABLE IF NOT EXISTS agent_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    query TEXT,
    retrieved_docs JSONB,
    reranked_docs JSONB,
    summary TEXT,
    self_eval_score FLOAT,
    feedback TEXT,
    feedback_score FLOAT,
    episodic_memory JSONB
);

-- 可选：创建向量索引表 (示例)
CREATE TABLE IF NOT EXISTS vector_index (
    id SERIAL PRIMARY KEY,
    doc_id TEXT,
    embedding VECTOR(1536),  -- Depends on the vector dimension you're using.
    metadata JSONB
);

-- Create a user interest profile.
CREATE TABLE IF NOT EXISTS user_profile (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    interests JSONB,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Prebuilt index for full-text search on query field.
CREATE INDEX IF NOT EXISTS idx_query ON agent_logs USING gin (to_tsvector('english', query));
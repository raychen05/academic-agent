# logger.py (advanced)

import os
import psycopg2
from datetime import datetime
import json

class AgentLogger:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            database=os.getenv("PG_DB"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            port=os.getenv("PG_PORT", 5432)
        )
        self.conn.autocommit = True

    def log_interaction(self, data: dict):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO agent_logs 
            (timestamp, query, retrieved_docs, reranked_docs, summary, self_eval_score, feedback, feedback_score, episodic_memory)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            datetime.utcnow(),
            data.get("query"),
            json.dumps(data.get("retrieved_docs")),
            json.dumps(data.get("reranked_docs")),
            data.get("summary"),
            data.get("self_eval_score"),
            data.get("feedback"),
            data.get("feedback_score"),
            json.dumps(data.get("episodic_memory"))
        ))
        cursor.close()
        print("[AgentLogger] Saved log to DB.")
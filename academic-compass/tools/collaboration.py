import sqlite3
import os
from typing import List, Dict, Optional

class CollaborationManager:
    def __init__(self, db_path="data/collaboration/comments.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paper_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def add_comment(self, paper_id: str, user_id: str, content: str) -> int:
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO comments (paper_id, user_id, content)
            VALUES (?, ?, ?)
        """, (paper_id, user_id, content))
        self.conn.commit()
        return cur.lastrowid

    def update_comment(self, comment_id: int, new_content: str) -> bool:
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE comments
            SET content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (new_content, comment_id))
        self.conn.commit()
        return cur.rowcount > 0

    def delete_comment(self, comment_id: int) -> bool:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def get_comments_by_paper(self, paper_id: str) -> List[Dict]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, paper_id, user_id, content, created_at, updated_at
            FROM comments
            WHERE paper_id = ?
            ORDER BY created_at ASC
        """, (paper_id,))
        rows = cur.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get_comments_by_user(self, user_id: str) -> List[Dict]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, paper_id, user_id, content, created_at, updated_at
            FROM comments
            WHERE user_id = ?
            ORDER BY created_at ASC
        """, (user_id,))
        rows = cur.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def _row_to_dict(self, row):
        return {
            "id": row[0],
            "paper_id": row[1],
            "user_id": row[2],
            "content": row[3],
            "created_at": row[4],
            "updated_at": row[5],
        }

    def close(self):
        self.conn.close()
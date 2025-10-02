import json
import time
from typing import List
import redis
from config import settings

r = redis.from_url(settings.REDIS_URL, decode_responses=True)

PREFIX = "st:"  # short-term channel per user
MAX_MESSAGES = 50  # max messages to keep per conversation

def add_message(conv_id: str, role: str, content: str, timestamp: float = None):
    timestamp = timestamp or time.time()
    item = json.dumps({"role": role, "content": content, "ts": timestamp})
    key = PREFIX + conv_id
    r.rpush(key, item)
    # trim by count
    r.ltrim(key, -MAX_MESSAGES, -1)

def get_messages(conv_id: str) -> List[dict]:
    key = PREFIX + conv_id
    raw = r.lrange(key, 0, -1)
    return [json.loads(x) for x in raw]

def clear(conv_id: str):
    r.delete(PREFIX + conv_id)
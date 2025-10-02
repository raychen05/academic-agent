# episodic.py

from collections import deque

class EpisodicMemory:
    """
    Short-term (episodic) memory to hold recent interactions.
    """

    def __init__(self, max_length=10):
        self.memory = deque(maxlen=max_length)

    def add_event(self, event: dict):
        self.memory.append(event)
        print(f"[EpisodicMemory] Added event: {event}")

    def get_recent_events(self):
        return list(self.memory)

    def clear(self):
        self.memory.clear()
        print("[EpisodicMemory] Cleared.")
# logger.py

import json
from datetime import datetime
import os

class AgentLogger:
    """
    Logs queries, responses, and evaluation data for continuous learning.
    """

    def __init__(self, log_file="agent_logs.jsonl"):
        self.log_file = log_file
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                pass  # Create empty file

    def log_interaction(self, data: dict):
        """
        Append a JSON line for each turn.
        """
        data["timestamp"] = datetime.utcnow().isoformat()
        with open(self.log_file, "a") as f:
            f.write(json.dumps(data) + "\n")
        print(f"[AgentLogger] Logged interaction at {data['timestamp']}")

    def read_logs(self):
        """
        Load all logs as a list.
        """
        with open(self.log_file, "r") as f:
            return [json.loads(line) for line in f if line.strip()]
# agent/state.py - Agent state model

from dataclasses import dataclass, field
from typing import List, Any

@dataclass
class AgentState:
    """
    Defines the runtime state of your Agent.
    """
    query: str = ""
    context_chunks: List[str] = field(default_factory=list)
    retrieved_chunks: List[str] = field(default_factory=list)
    answer: str = ""
    feedback: str = ""
    self_eval: Any = None
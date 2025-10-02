# agent/planner.py
# A simple reasoning loop:
# 	1.	Get query
# 	2.	Embed query → retrieve
# 	3.	Synthesize answer
# 	4.	Collect feedback & eval

from agent.memory import MemoryManager
from agent.state import AgentState
from agent.feedback import FeedbackHandler
from tools.semantic_search import SemanticSearchTool
from tools.co_writer import CoWriter
from dataclasses import dataclass


class Planner:
    def __init__(self):
        self.memory = MemoryManager()
        self.feedback_handler = FeedbackHandler(self.memory)
        self.search_tool = SemanticSearchTool(self.memory)
        self.writer = CoWriter()

    def plan_steps(self, state: AgentState):
        print(f"🚀 Received query: {state.query}")

        # 1️⃣ Embed query & retrieve
        query_embedding = self.search_tool.embed_query(state.query)
        retrieved_chunks = self.memory.search_index(query_embedding)
        state.retrieved_chunks = retrieved_chunks

        print(f"🔍 Retrieved: {retrieved_chunks}")

        # 2️⃣ Generate draft answer
        answer = self.writer.generate_answer(state.query, retrieved_chunks)
        state.answer = answer

        print(f"📝 Draft answer: {answer}")

        # 3️⃣ Collect feedback
        feedback = self.feedback_handler.collect_feedback(state)
        print(f"💡 User feedback: {feedback}")

        # 4️⃣ Self-evaluate
        score = self.feedback_handler.self_evaluate(state)
        print(f"🤖 Self-eval score: {score}")

        # 5️⃣ Store feedback
        self.feedback_handler.store_feedback(state)

        return answer
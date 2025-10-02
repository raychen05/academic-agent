# agent/feedback.py
# Handles user feedback + simple self-eval logic.

from agent.state import AgentState

class FeedbackHandler:
    def __init__(self, memory_manager, min_score=3.0, max_score=5.0, answer_length_threshold=50):
        """
        Args:
            memory_manager: an instance responsible for storing feedback
            min_score: self-eval score for short answers
            max_score: self-eval score for long answers
            answer_length_threshold: length threshold to assign max_score
        """
        self.memory_manager = memory_manager
        self.min_score = min_score
        self.max_score = max_score
        self.answer_length_threshold = answer_length_threshold

    def collect_feedback(self, state: AgentState):
        """
        Simulate getting user feedback — replace this with real UI input in production.
        Validates input to be between 1-5 stars.
        """
        while True:
            feedback = input("💬 Provide feedback (1-5 stars): ").strip()
            if feedback in {"1", "2", "3", "4", "5"}:
                state.feedback = feedback
                return feedback
            else:
                print("⚠️ Invalid input. Please enter a number between 1 and 5.")

    def self_evaluate(self, state: AgentState):
        """
        Basic self-evaluation: gives a higher score if the answer length exceeds a threshold.
        Updates state.self_eval with the score.
        """
        if not hasattr(state, "answer") or not isinstance(state.answer, str):
            score = self.min_score
        else:
            score = self.max_score if len(state.answer) > self.answer_length_threshold else self.min_score

        state.self_eval = score
        return score

    def store_feedback(self, state: AgentState):
        """
        Store feedback using the memory manager.
        Expects the state to have query, answer, feedback, and self_eval attributes.
        """
        self.memory_manager.store_feedback(
            query=state.query,
            answer=state.answer,
            feedback=state.feedback,
            score=state.self_eval
        )
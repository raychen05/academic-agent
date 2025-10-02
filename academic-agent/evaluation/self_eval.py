# self_eval.py

class SelfEvaluator:
    """
    Evaluates the quality of the agent's output.
    """

    def __init__(self):
        self.criteria_keywords = ["accurate", "complete", "relevant"]

    def evaluate(self, response: str) -> float:
        """
        Example: Score based on keyword presence.
        Replace with more advanced checks or LLM scoring.
        """
        score = 0
        for kw in self.criteria_keywords:
            if kw in response.lower():
                score += 0.3

        final_score = min(score, 1.0)  # Cap at 1.0
        print(f"[SelfEvaluator] Evaluation score: {final_score:.2f}")
        return final_score
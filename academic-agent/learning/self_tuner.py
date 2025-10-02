# self_tuner.py

class SelfTuner:
    """
    Adjusts the agent's internal parameters based on self-evaluation.
    """

    def __init__(self):
        self.learning_rate = 0.1  # Example tunable param
        self.quality_threshold = 0.75

    def adjust(self, eval_score: float):
        """
        Adjust parameters based on a score (e.g., from self-evaluation)
        """
        if eval_score < self.quality_threshold:
            # For example, increase learning rate to encourage faster adaptation
            self.learning_rate *= 1.1
        else:
            # If good, decay learning rate for stability
            self.learning_rate *= 0.95

        print(f"[SelfTuner] Adjusted learning rate to {self.learning_rate:.4f}")
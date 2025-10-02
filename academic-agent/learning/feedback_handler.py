# feedback_handler.py

class FeedbackHandler:
    """
    Handles user feedback and logs it for future improvement.
    """

    def __init__(self):
        self.feedback_log = []

    def store_feedback(self, user_feedback: str, context: dict):
        """
        Save feedback with optional context for traceability.
        """
        entry = {
            "feedback": user_feedback,
            "context": context
        }
        self.feedback_log.append(entry)
        print(f"[FeedbackHandler] Stored feedback: {entry}")

    def get_all_feedback(self):
        """
        Return all collected feedback.
        """
        return self.feedback_log
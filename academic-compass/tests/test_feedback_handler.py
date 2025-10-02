# tests/test_feedback_handler.py

import pytest
from unittest.mock import patch, MagicMock

from agent.state import AgentState
from agent.feedback import FeedbackHandler

'''
monkeypatch - Clean way to override input() during the test
MagicMock - Mocks your MemoryManager dependency
assert - Checks that FeedbackHandler updates AgentState correctly
.assert_called_once_with() - Confirms your memory saves the right values
'''


def test_collect_feedback(monkeypatch):
    memory_mock = MagicMock()
    handler = FeedbackHandler(memory_mock)
    state = AgentState(query="What is AI?")

    # Mock input() to simulate user feedback
    monkeypatch.setattr("builtins.input", lambda _: "5")

    feedback = handler.collect_feedback(state)

    assert feedback == "5"
    assert state.feedback == "5"

def test_self_evaluate_long_answer():
    memory_mock = MagicMock()
    handler = FeedbackHandler(memory_mock)
    state = AgentState(query="Test")
    state.answer = "This is a long answer that should get a high self-eval score because it exceeds the threshold length of 50 characters."

    score = handler.self_evaluate(state)

    assert score == 5.0
    assert state.self_eval == 5.0

def test_self_evaluate_short_answer():
    memory_mock = MagicMock()
    handler = FeedbackHandler(memory_mock)
    state = AgentState(query="Test")
    state.answer = "Short answer."

    score = handler.self_evaluate(state)

    assert score == 3.0
    assert state.self_eval == 3.0

def test_store_feedback():
    memory_mock = MagicMock()
    handler = FeedbackHandler(memory_mock)
    state = AgentState(query="What is NLP?")
    state.answer = "Natural Language Processing is..."
    state.feedback = "4"
    state.self_eval = 4.0

    handler.store_feedback(state)

    memory_mock.store_feedback.assert_called_once_with(
        query=state.query,
        answer=state.answer,
        feedback=state.feedback,
        score=state.self_eval
    )
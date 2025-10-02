# tests/test_planner.py

import pytest
from unittest.mock import MagicMock, patch
from agent.state import AgentState

''' 
@patch - Mocks each real dependency: MemoryManager, FeedbackHandler, SemanticSearchTool, CoWriter
MagicMock - Controls the outputs, e.g., search_index returns fake chunks
assert - Checks that Planner sets the state correctly and returns the right answer
.assert_called_once() - Confirms each tool step runs exactly once
'''


# ✅ Patch the dependent classes
@patch("agent.planner.MemoryManager")
@patch("agent.planner.FeedbackHandler")
@patch("agent.planner.SemanticSearchTool")
@patch("agent.planner.CoWriter")
def test_planner_plan_steps(mock_cowriter, mock_search_tool, mock_feedback_handler, mock_memory_manager):
    # Setup mocks
    mock_memory = MagicMock()
    mock_memory.search_index.return_value = ["chunk1", "chunk2"]

    mock_search = MagicMock()
    mock_search.embed_query.return_value = [0.1, 0.2, 0.3]

    mock_writer = MagicMock()
    mock_writer.generate_answer.return_value = "This is a test answer."

    mock_feedback = MagicMock()
    mock_feedback.collect_feedback.return_value = "Helpful feedback."
    mock_feedback.self_evaluate.return_value = 0.9

    # Wire up the patch returns
    mock_memory_manager.return_value = mock_memory
    mock_search_tool.return_value = mock_search
    mock_cowriter.return_value = mock_writer
    mock_feedback_handler.return_value = mock_feedback

    # Import here to use patched Planner
    from agent.planner import Planner

    planner = Planner()
    state = AgentState(query="What is AI?")

    answer = planner.plan_steps(state)

    # ✅ Assertions
    assert isinstance(answer, str)
    assert answer == "This is a test answer."
    assert state.retrieved_chunks == ["chunk1", "chunk2"]
    assert state.answer == "This is a test answer."

    mock_search.embed_query.assert_called_once_with(state.query)
    mock_memory.search_index.assert_called_once()
    mock_writer.generate_answer.assert_called_once()
    mock_feedback.collect_feedback.assert_called_once()
    mock_feedback.self_evaluate.assert_called_once()
    mock_feedback.store_feedback.assert_called_once_with(state)
# scripts/test_co_writer.py
# tests/test_co_writer.py

import pytest
from tools.co_writer import CoWriter
from unittest.mock import patch, MagicMock


@patch("tools.co_writer.OpenAI")  # 👈 Path to what you import in your module
def test_generate_section_with_mock(mock_openai):
    # Setup fake response
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "This is a mocked introduction section."
    mock_response.choices = [mock_choice]

    # Wire fake chain: chat.completions.create() returns mock_response
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client

    writer = CoWriter()
    result = writer.generate_section("AI for Climate", "introduction")

    assert isinstance(result, str)
    assert "mocked introduction" in result

    # Verify your LLM client was actually called once
    mock_client.chat.completions.create.assert_called_once()

def test_generate_introduction():
    writer = CoWriter()
    topic = "AI for Climate Modeling"
    result = writer.generate_section(topic, "introduction")

    assert isinstance(result, str)
    assert "introduction" in result.lower() or "introduce" in result.lower()

def test_generate_related_work():
    writer = CoWriter()
    topic = "NLP for Legal Texts"
    result = writer.generate_section(topic, "related work")

    assert isinstance(result, str)
    assert "related work" in result.lower() or "review" in result.lower()

def test_unsupported_section():
    writer = CoWriter()
    topic = "Quantum Computing"
    result = writer.generate_section(topic, "unknown")

    assert "not implemented" in result.lower()
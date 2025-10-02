import pytest
from agent.memory import MemoryManager
from agent.self_learning import SelfLearningAgent

@pytest.fixture
def agent():
    memory = MemoryManager()
    return SelfLearningAgent(memory)

def test_store_and_retrieve_profile(agent):
    agent.store_user_profile(
        user_id="bob",
        interests=["quantum computing", "cryptography"],
        preferences={"format": "brief", "language": "English"}
    )

    profile = agent.retrieve_user_profile("bob")
    assert "quantum computing" in profile
    assert "cryptography" in profile

def test_recommend(agent):
    agent.store_user_profile(
        user_id="carol",
        interests=["bioinformatics"],
        preferences={"depth": "high"}
    )

    answer = agent.recommend("carol", "What are hot topics in genomics?")
    assert "bioinformatics" in answer
    assert "What are hot topics" in answer
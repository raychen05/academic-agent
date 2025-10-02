# test_pipeline.py

from agent.planner import Planner

def test_sample_query():
    planner = Planner()
    state = {"query": "What is the trend in AI for climate change?"}
    result = planner.plan_steps(state)
    assert result is not None, "Planner should return a result"
    print("✅ Passed: test_sample_query")

if __name__ == "__main__":
    test_sample_query()
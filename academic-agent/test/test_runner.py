# test_runner.py

import yaml
from agent.run_agent import ResearchExpertAgent

def run_tests():
    agent = ResearchExpertAgent()
    with open("test_prompts.yaml", "r") as f:
        test_prompts = yaml.safe_load(f)

    for prompt in test_prompts:
        query = prompt["query"]
        print(f"\n🔍 Query: {query}")
        summary, eval_score = agent.process_query(query)
        print(f"✅ Summary: {summary}")
        print(f"🔎 Self-Eval Score: {eval_score:.2f}")

if __name__ == "__main__":
    run_tests()


# To run this test script, ensure you have a `test_prompts.yaml` file with the following structure:
# test_prompts.yaml 
# Run: python test_runner.py
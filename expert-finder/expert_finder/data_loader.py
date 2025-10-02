import json

def load_expert_profiles():
    with open("data/sample_experts.json", "r") as f:
        return json.load(f)

# run.py
# This is a simple CLI runner that lets you call different modes —
# like running the planner, or testing the pipeline.
#  Usage:
# python run.py --query "What is the trend in deep learning for climate science?"



import argparse
from agent.planner import Planner

def main():
    parser = argparse.ArgumentParser(description="ResearchCompass Runner")
    parser.add_argument(
        "--query",
        type=str,
        help="Your research question"
    )

    args = parser.parse_args()

    if args.query:
        planner = Planner()
        state = {"query": args.query}
        result = planner.plan_steps(state)
        print(f"🔍 Query: {args.query}")
        print(f"🧠 Agent answer: {result or 'No result yet (stub).'}")
    else:
        print("Please provide a --query argument.")

if __name__ == "__main__":
    main()
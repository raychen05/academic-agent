# run_agent.py

import openai
import yaml
from retrievers.grant_retriever import GrantRetriever
from retrievers.reranker import Reranker
from learning.feedback_handler import FeedbackHandler
from learning.self_tuner import SelfTuner
from learning.logger import AgentLogger
from evaluation.self_eval import SelfEvaluator
from memory.long_term import LongTermMemory
from memory.episodic import EpisodicMemory


class ResearchExpertAgent:
    """
    Orchestrates the expert reasoning loop.
    """

    def __init__(self, config_path="config.yaml"):
        # Load configs
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        openai.api_key = config["OPENAI_API_KEY"]

        self.retriever = GrantRetriever()
        self.reranker = Reranker()
        self.feedback_handler = FeedbackHandler()
        self.self_tuner = SelfTuner()
        self.self_evaluator = SelfEvaluator()
        self.long_term_memory = LongTermMemory()
        self.episodic_memory = EpisodicMemory()
        self.logger = AgentLogger()

    def process_query(self, query: str):
        # Your existing loop: retrieve → rerank → summarize → eval → tune


        # 1. Retrieve relevant documents
        retrieved_docs = self.retriever.retrieve(query)

        # 2. Rerank retrieved docs
        reranked_docs = self.reranker.rerank(query, retrieved_docs)

        # 3. Store to episodic memory
        self.episodic_memory.add_event({
            "query": query,
            "docs": reranked_docs
        })

        # 4. Summarize using GPT-4
        summary = self._summarize(reranked_docs)

        # 5. Evaluate response quality
        eval_score = self.self_evaluator.evaluate(summary)

        # 6. Self-tune parameters
        self.self_tuner.adjust(eval_score)

        # Log the entire turn
        self.logger.log_interaction({
            "query": query,
            "retrieved_docs": retrieved_docs,
            "reranked_docs": reranked_docs,
            "summary": summary,
            "self_eval_score": eval_score,
            "episodic_memory": self.episodic_memory.get_recent_events()
        })

        return summary, eval_score

    def _summarize(self, docs):
        """
        Uses OpenAI GPT-4 to summarize the top docs.
        """
        top_docs = "\n\n".join([doc[0] for doc in docs[:3]])
        prompt = f"Summarize the following research grant documents in a concise, relevant, and accurate way:\n\n{top_docs}\n\nSummary:"

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a research grant expert summarizer."},
                {"role": "user", "content": prompt}
            ]
        )
        summary = response.choices[0].message["content"].strip()
        print(f"[ResearchExpertAgent] Generated summary:\n{summary}")
        return summary

    def store_feedback(self, feedback: str):
        context = {
            "episodic_memory": self.episodic_memory.get_recent_events(),
            "long_term_memory_keys": list(self.long_term_memory.all().keys())
        }
        self.feedback_handler.store_feedback(feedback, context)

        # Log feedback for traceability
        self.logger.log_interaction({
            "feedback": feedback,
            "context": context
        })
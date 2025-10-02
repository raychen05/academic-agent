# tools/experiment_aggregator.py
# Extracts structured experimental details from dummy sections or tables.

# tools/experiment_aggregator.py

class ExperimentAggregator:
    def __init__(self):
        """
        Example: Preload dummy experiments.
        In production, you’d parse PDFs, JSON-LD, or tables with section taggers.
        """
        self.experiments = [
            {
                "paper": "Deep Learning for Genomics",
                "authors": ["Alice Smith", "Bob Chen"],
                "dataset": "1000 Genomes",
                "method": "Transformer Encoder",
                "metrics": {"Accuracy": "92%"},
                "year": 2022
            },
            {
                "paper": "Climate Trend Detection",
                "authors": ["Maria Lopez"],
                "dataset": "MODIS Remote Sensing",
                "method": "CNN + LSTM",
                "metrics": {"RMSE": "0.15"},
                "year": 2021
            },
            {
                "paper": "LLMs for Legal Analysis",
                "authors": ["Yuki Tanaka"],
                "dataset": "US Supreme Court Opinions",
                "method": "GPT-4",
                "metrics": {"F1": "88%"},
                "year": 2024
            }
        ]

    def list_experiments(self, topic: str) -> list:
        """
        Return experiments where the topic appears in the paper title, dataset, or method.
        """
        topic_lower = topic.lower()
        return [
            exp for exp in self.experiments
            if topic_lower in exp["paper"].lower()
            or topic_lower in exp["dataset"].lower()
            or topic_lower in exp["method"].lower()
        ]

    def aggregate_summary(self, topic: str) -> dict:
        """
        Provide a simple aggregate view:
        - Number of experiments found
        - Common methods
        - Common datasets
        """
        matches = self.list_experiments(topic)
        if not matches:
            return {"message": "No experiments found for this topic."}

        methods = [exp["method"] for exp in matches]
        datasets = [exp["dataset"] for exp in matches]

        return {
            "topic": topic,
            "num_experiments": len(matches),
            "methods": list(set(methods)),
            "datasets": list(set(datasets)),
        }
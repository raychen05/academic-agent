import pandas as pd
from typing import List, Dict
import matplotlib.pyplot as plt

class TrendDetector:
    def __init__(self):
        pass

    def normalize_topics(self, topics: List[str]) -> List[str]:
        """
        Basic topic normalization: lowercasing, stripping whitespace.
        You could expand this with lemmatization or embeddings.
        """
        return [topic.strip().lower() for topic in topics]

    def detect_trends(self, records: List[Dict], min_count: int = 5) -> pd.DataFrame:
        """
        records: list of {"year": int, "topic": str}
        Returns a DataFrame with counts per year and topic.
        """
        # Normalize
        for r in records:
            r["topic"] = r["topic"].strip().lower()

        df = pd.DataFrame(records)
        trends = df.groupby(["topic", "year"]).size().reset_index(name="count")

        # Filter low-frequency topics
        topic_totals = trends.groupby("topic")["count"].sum().reset_index()
        frequent_topics = topic_totals[topic_totals["count"] >= min_count]["topic"]
        trends = trends[trends["topic"].isin(frequent_topics)]

        return trends

    def plot_trend(self, trends: pd.DataFrame, topic: str):
        """
        Simple line plot for a given topic's counts over time.
        """
        df_topic = trends[trends["topic"] == topic.lower()]
        if df_topic.empty:
            print(f"No data for topic: {topic}")
            return

        df_topic = df_topic.sort_values("year")
        plt.figure(figsize=(8, 5))
        plt.plot(df_topic["year"], df_topic["count"], marker="o")
        plt.title(f"Trend for '{topic}'")
        plt.xlabel("Year")
        plt.ylabel("Publication Count")
        plt.grid(True)
        plt.show()

    def emerging_topics(self, trends: pd.DataFrame, recent_years: int = 3, growth_threshold: float = 0.2) -> List[str]:
        """
        Identify emerging topics based on percentage growth in the recent N years.
        """
        max_year = trends["year"].max()
        recent = trends[trends["year"] >= max_year - recent_years + 1]

        topic_growth = recent.groupby("topic")["count"].sum().reset_index()
        topic_growth = topic_growth.sort_values("count", ascending=False)

        # For simplicity, return topics above a threshold count change
        emerging = topic_growth[topic_growth["count"] >= growth_threshold * topic_growth["count"].max()]
        return emerging["topic"].tolist()
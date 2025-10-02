# dashboard.py

import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="Research Expert Agent Logs Dashboard", layout="wide")

st.title("📊 Research Expert Agent - Logs Dashboard")

# Load your JSONL logs
LOG_FILE = "agent_logs.jsonl"

@st.cache_data
def load_logs():
    data = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            data.append(json.loads(line))
    return pd.json_normalize(data)

try:
    df = load_logs()

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Show raw logs table
    with st.expander("🔍 Raw Logs"):
        st.dataframe(df)

    # Self-eval score trend
    if "self_eval_score" in df.columns:
        st.subheader("📈 Self-Evaluation Score Over Time")
        st.line_chart(df.set_index("timestamp")["self_eval_score"])

        avg_score = df["self_eval_score"].mean()
        st.metric(label="Average Self-Eval Score", value=f"{avg_score:.2f}")

    # Top queries
    st.subheader("🔎 Most Frequent Queries")
    query_counts = df["query"].value_counts().reset_index()
    query_counts.columns = ["query", "count"]
    st.bar_chart(query_counts.set_index("query"))

    # Feedback log
    feedbacks = df[df["feedback"].notnull()]
    st.subheader("🗣️ Feedback Collected")
    st.write(feedbacks[["timestamp", "feedback"]])

    # Retrieved docs summary
    st.subheader("📚 Retrieved Docs Examples")
    st.write(df[["query", "retrieved_docs"]].tail(5))

except Exception as e:
    st.warning(f"Could not load logs: {e}")
    st.info("Make sure you have run some queries to generate `agent_logs.jsonl`.")


##  run: streamlit run dashboard.py

'''
With the dashboard, you can:
✅ Spot low-scoring answers → improve prompts or reranker logic
✅ See which queries are popular → precompute for faster results
✅ Check feedback → cluster recurring user issues
✅ Export logs → use them as training data for prompt tuning or model finetuning

✅ Bonus: Save to CSV
df.to_csv("agent_logs.csv", index=False)
'''
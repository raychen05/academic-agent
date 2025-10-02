# src/normalizer/eval/metrics.py
import pandas as pd

def top1_accuracy(df: pd.DataFrame):
    return (df["pred_id"] == df["gold_id"]).mean()

def mrr(df: pd.DataFrame):
    return df["reciprocal_rank"].mean()

# src/normalizer/eval/evaluate.py
# Expect data/eval/labeled_pairs.csv: input_name,entity_type,gold_id,context(json)
import json, pandas as pd
from ..pipeline import NormalizationPipeline

def run_eval():
    df = pd.read_csv("data/eval/labeled_pairs.csv")
    pipe = NormalizationPipeline()
    preds = []
    for _, r in df.iterrows():
        ctx = json.loads(r.get("context","{}"))
        out = pipe.normalize(r["entity_type"], r["input_name"], ctx)
        preds.append({"pred_id": out.get("id"), "pred_name": out.get("name"), "score": out.get("score",0.0)})
    out_df = pd.concat([df, pd.DataFrame(preds)], axis=1)
    print("Top-1 acc:", (out_df["pred_id"] == out_df["gold_id"]).mean())
    out_df.to_csv("data/eval/predictions.csv", index=False)

if __name__ == "__main__":
    run_eval()

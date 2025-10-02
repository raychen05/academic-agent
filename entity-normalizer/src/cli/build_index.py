import pandas as pd, faiss, numpy as np
from sentence_transformers import SentenceTransformer
import argparse

def build(csv_path, name_col, out_path, model_name="BAAI/bge-small-en"):
    df = pd.read_csv(csv_path)
    names = df[name_col].astype(str).tolist()
    model = SentenceTransformer(model_name)
    X = model.encode(names, normalize_embeddings=True)
    index = faiss.IndexFlatIP(X.shape[1]); index.add(X)
    faiss.write_index(index, out_path)
    np.save(out_path.replace(".faiss",".ids.npy"), np.arange(len(names)))
    print("Saved", out_path)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--name_col", default="name")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="BAAI/bge-small-en")
    args = ap.parse_args()
    build(args.csv, args.name_col, args.out, args.model)

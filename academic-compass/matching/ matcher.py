import pandas as pd
from .normalize import normalize_name
from .vector_index import OrgVectorIndex
from .rerank import fuzzy_rerank

class OrgMatcher:
    def __init__(self, csv_path="data/org_names.csv"):
        df = pd.read_csv(csv_path)
        self.canon_map = {}
        all_names = []
        for _, row in df.iterrows():
            norm = normalize_name(row["variant"])
            self.canon_map[norm] = row["canonical"]
            all_names.append(norm)
        self.index = OrgVectorIndex()
        self.index.build(all_names)

    def match(self, user_input):
        norm = normalize_name(user_input)
        top_candidates = self.index.search(norm, top_k=10)
        reranked = fuzzy_rerank(norm, top_candidates)
        best = reranked[0][0] if reranked else top_candidates[0][0]
        return {
            "input": user_input,
            "normalized": norm,
            "match": best,
            "canonical": self.canon_map.get(best, best)
        }


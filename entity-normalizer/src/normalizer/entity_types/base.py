# src/normalizer/entity_types/base.py
from ..candidates.faiss_index import FaissSearcher
from ..candidates.generator import gen_candidates
from ..ranking.context_features import ctx_score
from ..ranking.reranker import final_score
from ..stores.catalog import Catalog
from ..config import CFG

class BaseNormalizer:
    def __init__(self, entity: str, catalog_path: str):
        self.entity = entity
        self.catalog = Catalog(catalog_path)
        self.searcher = FaissSearcher(self.catalog.names, CFG.model_name)

    def normalize(self, text: str, user_ctx: dict | None = None):
        user_ctx = user_ctx or {}
        w = CFG.weights[self.entity]
        cands = gen_candidates(text, self.catalog.names, self.searcher)
        best = None
        for cand_name, embed_mix in cands[:50]:
            row = self.catalog.row_by_name(cand_name)
            ctxs = ctx_score(self.entity, user_ctx, row)
            score = final_score(text, cand_name, embed_mix, ctxs, w)
            if not best or score > best["score"]:
                best = {"name": cand_name, "id": row.get("id"), "score": score, "row": row}
        return best if best and best["score"] >= w["threshold"] else {"name": None, "id": None, "score": best["score"] if best else 0.0}

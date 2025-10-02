# concept_adoption.py
from typing import List, Dict, Any, Tuple
import re
import numpy as np
import math
from collections import Counter, defaultdict
from sentence_transformers import SentenceTransformer, util

# Optional: spaCy for noun-phrase extraction (fallback to regex n-grams if not available)
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

# Embedding model (lightweight for demo; swap for higher-capacity in prod)
EMB_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# ----------------------
# Utilities / Extraction
# ----------------------

def simple_tokenize(text: str) -> List[str]:
    # simple whitespace tokenizer + lower
    return [t.lower() for t in re.findall(r"\b\w[\w\-\_]+\b", text)]

def extract_ngrams(text: str, n_min=1, n_max=4, min_freq=1) -> Counter:
    """
    Extract candidate n-grams from text.
    Returns Counter(ngram -> count).
    """
    tokens = simple_tokenize(text)
    c = Counter()
    L = len(tokens)
    for n in range(n_min, min(n_max, L)+1):
        for i in range(L - n + 1):
            ng = " ".join(tokens[i:i+n])
            # simple filter: remove stop-ish tokens and extremely common single words
            if re.search(r'^[0-9]+$', ng):
                continue
            if len(ng) < 3:
                continue
            c[ng] += 1
    # filter by min_freq
    return Counter({k:v for k,v in c.items() if v >= min_freq})

def extract_noun_phrases(text: str, min_len=2) -> List[str]:
    """
    Extract noun phrases using spaCy if available; fallback to n-grams.
    """
    if nlp:
        doc = nlp(text)
        phrases = []
        for np in doc.noun_chunks:
            s = np.text.strip().lower()
            if len(s.split()) >= min_len:
                phrases.append(s)
        return phrases
    else:
        # fallback: return common 2-3 grams
        ng = extract_ngrams(text, n_min=2, n_max=3, min_freq=1)
        return list(ng.keys())

def detect_formulae(text: str) -> List[str]:
    """
    Quick heuristic to find formula-like patterns e.g., "Eq. (1)", "E=mc^2", "f(x) =".
    """
    patterns = [
        r"[A-Za-z]\s*=\s*[A-Za-z0-9\^\+\-\*\/\(\)\[\]\.]+",
        r"Eq\.\s*\(?\d+\)?",
        r"equation\s*\(?\d+\)?",
        r"\\begin\{equation\}.*?\\end\{equation\}"
    ]
    found = set()
    for p in patterns:
        for m in re.findall(p, text, flags=re.IGNORECASE | re.DOTALL):
            found.add(m.strip())
    return list(found)

# ----------------------
# Embedding helpers
# ----------------------

def embed_texts(texts: List[str]) -> np.ndarray:
    if not texts:
        return np.zeros((0, EMB_MODEL.get_sentence_embedding_dimension()))
    return EMB_MODEL.encode(texts, convert_to_numpy=True, show_progress_bar=False)

def deduplicate_candidates(candidates: List[str], threshold: float = 0.85) -> List[str]:
    """
    Deduplicate list of phrase candidates using embeddings:
      - If two candidates have cosine similarity >= threshold, keep the longer/more frequent one.
    Returns list of representative candidates.
    """
    if not candidates:
        return []
    embs = embed_texts(candidates)
    keep = []
    used = set()
    sims = util.cos_sim(embs, embs).cpu().numpy()
    # score by length (longer / more tokens prioritized)
    scores = [len(c.split()) for c in candidates]
    order = sorted(range(len(candidates)), key=lambda i: (-scores[i], i))
    for idx in order:
        if idx in used:
            continue
        keep.append(candidates[idx])
        # mark others as used if similar
        for j in range(len(candidates)):
            if j == idx or j in used:
                continue
            if sims[idx, j] >= threshold:
                used.add(j)
    return keep

# ----------------------
# Matching / reuse detection
# ----------------------

def exact_ngram_match_count(ngram: str, doc_text: str) -> int:
    """
    Count exact n-gram occurrences (case-insensitive) in doc_text.
    """
    return len(re.findall(r"\b" + re.escape(ngram) + r"\b", doc_text, flags=re.IGNORECASE))

def semantic_match(phrase: str, doc_text: str, doc_emb: np.ndarray, phrase_emb: np.ndarray, sim_threshold: float = 0.72) -> bool:
    """
    Heuristic semantic match: embed (phrase) and doc_text (or its sentences) and check if any sentence has sim>=threshold.
    doc_emb can be a precomputed array of sentence embeddings for the doc.
    For speed, we provide doc_emb (num_sentences x D).
    """
    if doc_emb is None or doc_emb.shape[0] == 0:
        return False
    sims = util.cos_sim(phrase_emb, doc_emb).cpu().numpy().flatten()
    return bool((sims >= sim_threshold).any())

def build_doc_sentence_embeddings(doc_text: str) -> Tuple[List[str], np.ndarray]:
    """
    Split doc into sentences and embed them. Return (sentences, embeddings).
    Uses a naive sentence splitter.
    """
    # naive split by punctuation; swap to nltk.sent_tokenize if available
    sents = [s.strip() for s in re.split(r'(?<=[\.\?\!])\s+', doc_text) if s.strip()]
    if not sents:
        return [], np.zeros((0, EMB_MODEL.get_sentence_embedding_dimension()))
    embs = embed_texts(sents)
    return sents, embs

# ----------------------
# Main function
# ----------------------

def build_candidate_concepts(paper_text: str, top_k_ngrams=60, ngram_min_freq=1) -> List[str]:
    """
    Extract candidate concept phrases combining noun-phrases, n-grams, formulae.
    Returns deduplicated representative candidates.
    """
    ngram_counts = extract_ngrams(paper_text, n_min=1, n_max=4, min_freq=ngram_min_freq)
    top_ngrams = [ng for ng,_ in ngram_counts.most_common(top_k_ngrams)]

    noun_phrases = extract_noun_phrases(paper_text, min_len=1)
    formulae = detect_formulae(paper_text)

    combined = list(dict.fromkeys(top_ngrams + noun_phrases + formulae))  # preserve order, dedupe
    # dedupe semantically
    candidates = deduplicate_candidates(combined, threshold=0.86)
    return candidates

def compute_concept_adoption(paper: Dict[str, Any], citations: List[Dict[str, Any]],
                             sim_threshold_semantic: float = 0.72,
                             semantic_count_threshold: int = 1) -> Dict[str, Any]:
    """
    Main pipeline:
      - extract candidate concepts from the focal paper
      - for each candidate, compute exact and semantic reuse counts across citations
    citations: list of dicts with keys: 'title','abstract','year','text' (optional), etc.
    Returns detailed per-concept stats and overall index.
    """
    paper_text = (paper.get("title","") + "\n\n" + paper.get("abstract","")).strip()
    candidates = build_candidate_concepts(paper_text)

    # precompute embeddings for candidates
    cand_embs = embed_texts(candidates)

    # prepare citations: for each citation build a combined text and sentence embeddings
    prepared = []
    for c in citations:
        text = c.get("text") or (c.get("title","") + "\n\n" + c.get("abstract",""))
        sents, sent_embs = build_doc_sentence_embeddings(text)
        prepared.append({"meta": c, "text": text, "sents": sents, "sent_embs": sent_embs})

    # per-concept stats
    concept_stats = {}
    for idx, concept in enumerate(candidates):
        cemb = cand_embs[idx:idx+1]
        exact_count = 0
        semantic_count = 0
        first_year = None
        years = []
        matched_docs = []
        for doc in prepared:
            ex = exact_ngram_match_count(concept, doc["text"])
            sem = 0
            if not ex:
                # semantic match
                if semantic_match(concept, doc["text"], doc["sent_embs"], cemb, sim_threshold_semantic):
                    sem = 1
            used = ex or sem
            if used:
                semantic_count += sem
                exact_count += ex
                y = doc["meta"].get("year")
                if y:
                    years.append(y)
                    if first_year is None or y < first_year:
                        first_year = y
                matched_docs.append({"meta": doc["meta"], "exact_matches": ex, "semantic_match": bool(sem)})
        total_matches = len(matched_docs)
        # adoption velocity: matches per year since publication (if year present)
        pub_year = paper.get("year")
        if pub_year and years:
            span_years = max(1, max(years) - min(years) + 1)
            velocity = total_matches / span_years
        elif years:
            velocity = total_matches / max(1, len(set(years)))
        else:
            velocity = 0.0

        concept_stats[concept] = {
            "concept": concept,
            "exact_count": exact_count,
            "semantic_count": semantic_count,
            "total_matches": total_matches,
            "first_year": first_year,
            "years": sorted(list(set(years))),
            "velocity": round(velocity, 3),
            "matched_docs": matched_docs
        }

    # Aggregate into a Concept Adoption Index (CAI)
    # idea: weight concepts by novelty (longer / rare) and adoption frequency
    # novelty proxy: inverse frequency of concept across external corpus unknown => use concept length as proxy
    def novelty_proxy(concept_str: str) -> float:
        # length & token uniqueness heuristic
        toks = concept_str.split()
        return min(1.0, (len(toks) / 6.0))  # 1.0 for phrases >=6 tokens

    # compute raw component per concept
    raw_scores = []
    for c, stats in concept_stats.items():
        adoption = stats["total_matches"]  # raw reuse
        novelty = novelty_proxy(c)
        raw = novelty * (1 + math.log(1 + adoption))  # logarithmic scaling on adoption
        raw_scores.append((c, raw))

    # normalize raw to 0..1
    if raw_scores:
        vals = np.array([r for _,r in raw_scores], dtype=float)
        minv, maxv = vals.min(), vals.max()
        rangev = max(1e-9, maxv - minv)
        norm = {c: float((r-minv)/rangev) for (c,r) in raw_scores}
    else:
        norm = {}

    # concept adoption index = weighted average of normalized concept scores (weights: novelty)
    weights = []
    for c in concept_stats:
        w = novelty_proxy(c)
        weights.append(w)
    total_w = sum(weights) or 1.0
    cai = 0.0
    for c in concept_stats:
        cai += (weights.pop(0) / total_w) * norm.get(c, 0.0)
    cai = round(float(cai) * 100, 2)  # scale 0..100

    # Prepare top concepts sorted by total_matches then semantic_count
    top_concepts = sorted(concept_stats.values(), key=lambda x: (x["total_matches"], x["semantic_count"], len(x["concept"].split())), reverse=True)

    return {
        "paper": {"title": paper.get("title"), "doi": paper.get("doi"), "year": paper.get("year")},
        "n_candidates": len(candidates),
        "n_citations": len(citations),
        "cai": cai,
        "concepts": top_concepts,
        "normalized_scores": norm
    }

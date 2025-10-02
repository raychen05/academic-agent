# diffusion.py
from typing import List, Dict, Any, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer, util
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from collections import Counter, defaultdict
import math
import datetime

# Load embedding model (choose lightweight model for speed in demo)
_EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------
# Utilities
# -------------------------
def embed_texts(texts: List[str]) -> np.ndarray:
    """Return numpy array of embeddings for a list of texts."""
    if not texts:
        return np.zeros((0, _EMBED_MODEL.get_sentence_embedding_dimension()))
    embs = _EMBED_MODEL.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return embs

def cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    """1 - cosine_similarity"""
    return 1.0 - util.cos_sim(a, b).item()

# -------------------------
# Data source stub
# -------------------------
def fetch_citations(paper_id: str) -> List[Dict[str, Any]]:
    """
    Replace this stub with production fetchers (OpenAlex / Semantic Scholar / CrossRef / internal DB).
    Each citation dict should contain at least:
      - 'title', 'abstract' (or concatenated text)
      - 'year' (int)
      - 'venue' (str)
      - 'affiliations': list of { 'institution': str, 'country': str }
      - 'language': str (e.g., 'en', 'zh', 'es')
      - 'doi' optional
    For demo, return a small synthetic list.
    """
    # Demo synthetic data
    return [
        {
            "title": "Follow-up on transformers for chemistry",
            "abstract": "Applies transformers to reaction prediction...",
            "year": 2023,
            "venue": "Chem AI",
            "affiliations": [{"institution": "Univ X", "country": "US"}],
            "language": "en"
        },
        {
            "title": "应用变换器在量子化学中的实现",
            "abstract": "中文描述：使用变换器近似DFT...",
            "year": 2024,
            "venue": "中国化学杂志",
            "affiliations": [{"institution": "Univ Y", "country": "CN"}],
            "language": "zh"
        },
        # add more synthetic or real citation records here...
    ]

# -------------------------
# Core diffusion calculations
# -------------------------
def build_citation_corpus(paper: Dict[str, Any], citations: List[Dict[str, Any]]) -> Tuple[List[str], np.ndarray, np.ndarray]:
    """
    Returns:
      - texts: list of textual items (paper + citations)
      - emb_all: embeddings array (N x D) aligned with texts
      - emb_paper: embedding vector for the focal paper
    """
    paper_text = (paper.get("title","") + "\n\n" + paper.get("abstract","")).strip()
    citation_texts = []
    for c in citations:
        text = (c.get("title","") + "\n\n" + c.get("abstract","")).strip()
        citation_texts.append(text)
    texts = [paper_text] + citation_texts
    emb_all = embed_texts(texts)
    emb_paper = emb_all[0:1, :]
    return texts, emb_all, emb_paper

def topic_projection(embeddings: np.ndarray, n_components: int = 2) -> np.ndarray:
    """Project embeddings to 2D using PCA (fast & stable)."""
    if embeddings.shape[0] <= 2:
        return embeddings[:, :2] if embeddings.shape[1] >= 2 else np.hstack([embeddings, np.zeros((embeddings.shape[0], 2-embeddings.shape[1]))])
    pca = PCA(n_components=n_components)
    coords = pca.fit_transform(embeddings)
    # normalize coords to [-1,1]
    coords = coords - coords.mean(axis=0)
    maxabs = np.max(np.abs(coords)) or 1.0
    coords = coords / maxabs
    return coords

def cluster_topics(embeddings: np.ndarray, k: int = 4) -> List[int]:
    """KMeans clusters (return labels). If few points, return zeros."""
    n = embeddings.shape[0]
    if n <= 1:
        return [0] * n
    k = min(k, max(1, n//2))
    km = KMeans(n_clusters=k, random_state=42)
    labels = km.fit_predict(embeddings)
    return labels.tolist()

# -------------------------
# Metric computations
# -------------------------
def shannon_entropy(proportions: List[float]) -> float:
    ps = np.array([p for p in proportions if p > 0.0])
    if len(ps) == 0:
        return 0.0
    return -float(np.sum(ps * np.log(ps))) / math.log(2)  # bits (base-2) normalized not by max

def normalized_entropy(counter: Dict[Any, int]) -> float:
    total = sum(counter.values()) or 1
    props = [v/total for v in counter.values()]
    if not props:
        return 0.0
    # normalize to [0,1] by dividing by max possible log2(n)
    H = shannon_entropy(props)
    maxH = math.log(len(props), 2) if len(props) > 1 else 1.0
    return float(H / maxH) if maxH > 0 else 0.0

def compute_breadth_by_disciplines(citations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Input: citations with 'venue' or 'venue_subjects' or classification.
    Basic heuristic: map venues to disciplines by keyword (production-ready: call classification API).
    Output: dict with discipline_counts, discipline_entropy, n_disciplines
    """
    # naive keyword mapping for demo (replace with real classifier)
    venue_to_discipline = {
        "chem": "Chemistry", "bio": "Biology", "ml": "Computer Science", "phys": "Physics", "chemistry":"Chemistry"
    }
    counts = Counter()
    for c in citations:
        v = (c.get("venue") or "").lower()
        disc = "Other"
        for k, d in venue_to_discipline.items():
            if k in v:
                disc = d
                break
        counts[disc] += 1
    return {
        "discipline_counts": dict(counts),
        "discipline_entropy_norm": normalized_entropy(counts),
        "n_disciplines": len(counts)
    }

def compute_geographic_spread(citations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compute country coverage, entropy, and normalized spread.
    """
    country_counts = Counter()
    for c in citations:
        affs = c.get("affiliations", []) or []
        countries = {a.get("country") for a in affs if a.get("country")}
        if not countries:
            country_counts["Unknown"] += 1
        else:
            for co in countries:
                country_counts[co] += 1
    n_countries = len([k for k in country_counts.keys() if k != "Unknown"])
    entropy = normalized_entropy(country_counts)
    coverage = n_countries / (n_countries + 1)  # simple normalized coverage
    return {"country_counts": dict(country_counts), "country_entropy_norm": entropy, "n_countries": n_countries, "coverage": coverage}

def compute_language_spread(citations: List[Dict[str, Any]]) -> Dict[str, Any]:
    lang_counts = Counter([c.get("language","unknown") for c in citations])
    n_lang = len(lang_counts)
    entropy = normalized_entropy(lang_counts)
    return {"language_counts": dict(lang_counts), "language_entropy_norm": entropy, "n_languages": n_lang}

def compute_depth(emb_all: np.ndarray, emb_paper: np.ndarray) -> Dict[str, Any]:
    """
    Depth = average cosine distance of citing-paper embeddings to the paper embedding.
    Also compute 90th percentile distance (how far frontier reaches).
    """
    if emb_all.shape[0] <= 1:
        return {"avg_distance": 0.0, "p90_distance": 0.0}
    # emb_all[0] is paper; citations are emb_all[1:]
    citations_emb = emb_all[1:, :]
    paper_vec = emb_paper[0]
    # compute cosine similarities
    sims = util.cos_sim(citations_emb, paper_vec).cpu().numpy().flatten()
    dists = 1.0 - sims
    avg = float(np.mean(dists)) if len(dists)>0 else 0.0
    p90 = float(np.percentile(dists, 90)) if len(dists)>0 else 0.0
    # normalize distances to [0,1] (cosine similarity already in [-1,1]; distances in [0,2])
    avg_norm = min(max(avg/1.0, 0.0), 1.0)
    p90_norm = min(max(p90/1.0, 0.0), 1.0)
    return {"avg_distance": avg_norm, "p90_distance": p90_norm}

def compute_temporal_diffusion(citations: List[Dict[str, Any]], paper_year: int) -> Dict[str, Any]:
    """
    Compute how citations appear over years: early adoption vs late.
    Measures:
      - time_to_first_nonlocal (years until paper gets citations from other disciplines/countries) -> for simplicity not implemented
      - slope / spread: share of citations in early window (paper_year+1..paper_year+2) vs later
    """
    years = [c.get("year", paper_year) for c in citations]
    if not years:
        return {"early_share": 0.0, "median_year": paper_year}
    counts = Counter(years)
    total = sum(counts.values())
    early = sum(v for y,v in counts.items() if y <= paper_year + 2)
    early_share = early / total if total else 0.0
    median_year = int(np.median(years))
    return {"early_share": early_share, "median_year": median_year}

# -------------------------
# Aggregate Diffusion Score
# -------------------------
def compute_knowledge_diffusion_score(paper: Dict[str, Any], citations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Main function: compute multi-component diffusion metrics and aggregate into a single score (0-100).
    Returns detailed breakdown and visualization-ready data.
    """
    # Build corpora and embeddings
    texts, emb_all, emb_paper = build_citation_corpus(paper, citations)

    # Topic projection for plotting
    coords = topic_projection(emb_all)  # N x 2

    # Clustering in topic space (helps breadth measure)
    labels = cluster_topics(emb_all, k= min(6, max(1, emb_all.shape[0]//3)))

    # Metrics
    breadth = compute_breadth_by_disciplines(citations)
    geo = compute_geographic_spread(citations)
    lang = compute_language_spread(citations)
    depth = compute_depth(emb_all, emb_paper)
    temporal = compute_temporal_diffusion(citations, paper.get("year", datetime.datetime.now().year))

    # Compose normalized components (all between 0..1)
    comp_breadth = breadth["discipline_entropy_norm"]  # 0..1
    comp_geo = geo["country_entropy_norm"]  # 0..1
    comp_lang = lang["language_entropy_norm"]  # 0..1
    comp_depth = depth["avg_distance"]  # 0..1
    comp_temporal = 1.0 - temporal["early_share"]  # if early share high, diffusion slower -> lower long-term diffusion. invert as reasonable.

    # Weighted aggregation (tunable)
    w = {"breadth": 0.30, "geo": 0.20, "lang": 0.10, "depth": 0.25, "temporal": 0.15}
    # normalize weights sum to 1
    total_w = sum(w.values())
    weights = {k:v/total_w for k,v in w.items()}

    raw_score = (comp_breadth*weights["breadth"] +
                 comp_geo*weights["geo"] +
                 comp_lang*weights["lang"] +
                 comp_depth*weights["depth"] +
                 comp_temporal*weights["temporal"])

    # scale to 0..100
    diffusion_score = round(raw_score * 100, 2)

    # Format output
    result = {
        "paper": {"title": paper.get("title"), "doi": paper.get("doi"), "year": paper.get("year")},
        "n_citations": len(citations),
        "components": {
            "breadth": {"value": comp_breadth, **breadth},
            "geography": {"value": comp_geo, **geo},
            "language": {"value": comp_lang, **lang},
            "depth": {"value": comp_depth, **depth},
            "temporal": {"value": comp_temporal, **temporal}
        },
        "weights": weights,
        "diffusion_score": diffusion_score,
        "coords": coords.tolist(),   # for visualization: first point is paper, others are citations
        "labels": labels,
        "raw_components": {
            "comp_breadth": comp_breadth,
            "comp_geo": comp_geo,
            "comp_lang": comp_lang,
            "comp_depth": comp_depth,
            "comp_temporal": comp_temporal
        }
    }
    return result

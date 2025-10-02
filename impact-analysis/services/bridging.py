# bridging.py
from typing import List, Dict, Any, Tuple
import numpy as np
from collections import Counter, defaultdict
from sentence_transformers import SentenceTransformer, util
import math
import networkx as nx

# Lightweight embedding model for field names
_EMB_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------
# Stubs: replace with real API fetchers
# -------------------------
def fetch_citations_with_fields(paper_id_or_doi: str) -> List[Dict[str, Any]]:
    """
    Replace with OpenAlex / Semantic Scholar / MAG call that returns citing papers and their 'fields' or 'concepts'.
    Minimal returned fields per citing paper:
      - 'id' (optional)
      - 'title'
      - 'year'
      - 'fields': list of field strings (e.g., "Computer Science", "Biology", "Bioinformatics")
      - 'affiliations' (optional)
    Demo synthetic return:
    """
    return [
        {"id": "C1", "title": "Translational ML in genomics", "year": 2023, "fields": ["Computer Science", "Genomics"]},
        {"id": "C2", "title": "Protein design via transformers", "year": 2024, "fields": ["Biology", "Computer Science"]},
        {"id": "C3", "title": "Quantum chemistry benchmarks", "year": 2023, "fields": ["Chemistry"]},
        {"id": "C4", "title": "Bioinformatics pipelines", "year": 2022, "fields": ["Bioinformatics", "Software Engineering"]},
        {"id": "C5", "title": "Policy paper referencing methods", "year": 2024, "fields": ["Public Policy", "Health Policy"]},
    ]

# -------------------------
# Utilities
# -------------------------
def normalize_field(field: str) -> str:
    """Light normalization of field strings (lowercase, simple mapping)."""
    if not field:
        return "Unknown"
    f = field.strip().lower()
    # small mapping to canonical names
    mapping = {
        "cs": "computer science", "comp sci": "computer science", "bioinformatics": "bioinformatics",
        "genomics": "genomics", "biology": "biology", "chem": "chemistry", "chemistry": "chemistry",
        "public policy": "public policy", "health policy": "health policy", "software engineering": "software engineering"
    }
    return mapping.get(f, f).title()

def embed_fields(fields: List[str]) -> Dict[str, np.ndarray]:
    """Return embedding vector per unique field string."""
    unique = list(dict.fromkeys(fields))
    if not unique:
        return {}
    embs = _EMB_MODEL.encode(unique, convert_to_numpy=True, show_progress_bar=False)
    return {f: embs[i] for i, f in enumerate(unique)}

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    return float(util.cos_sim(a, b).item())

# -------------------------
# Core bridging measures
# -------------------------
def field_counts_from_citations(citations: List[Dict[str, Any]]) -> Counter:
    """
    Count occurrences of fields across all citing papers.
    If a citing paper has multiple fields, each field counts once for that citation.
    Returns Counter(field -> count)
    """
    c = Counter()
    for cit in citations:
        fields = cit.get("fields", []) or []
        for f in fields:
            c[normalize_field(f)] += 1
    return c

def compute_pairwise_field_distances(field_embs: Dict[str, np.ndarray]) -> Dict[Tuple[str,str], float]:
    """Compute symmetric distances between fields normalized to [0,1]."""
    keys = list(field_embs.keys())
    d = {}
    for i, a in enumerate(keys):
        for j, b in enumerate(keys):
            if j <= i: continue
            sim = cosine_sim(field_embs[a], field_embs[b])  # in [-1,1]
            dist = 1.0 - sim  # roughly in [0,2]; typical sim in [0,1] -> dist in [0,1]
            # clip to 0..1
            dist = max(0.0, min(1.0, dist))
            d[(a,b)] = dist
            d[(b,a)] = dist
    # distance to self = 0
    for k in keys:
        d[(k,k)] = 0.0
    return d

def weighted_mean_pairwise_distance(field_counts: Counter, distances: Dict[Tuple[str,str], float]) -> float:
    """
    Weighted average of pairwise distances where weights = product of normalized counts.
    For fields i,j with counts ci,cj and total T, weight = (ci/T)*(cj/T) (so sum weights = 1 - sum self-weights?).
    We compute sum_{i<j} w_ij * dist_ij and return.
    """
    fields = list(field_counts.keys())
    total = sum(field_counts.values()) or 1
    norm = {f: field_counts[f] / total for f in fields}
    score = 0.0
    for i, a in enumerate(fields):
        for j, b in enumerate(fields):
            if j <= i: continue
            w = norm[a] * norm[b]
            dist = distances.get((a,b), 0.0)
            score += w * dist
    # score in [0,1]
    return float(max(0.0, min(1.0, score)))

def field_entropy(field_counts: Counter) -> float:
    """Normalized entropy across field distribution (0..1)."""
    total = sum(field_counts.values()) or 1
    ps = [v/total for v in field_counts.values() if v>0]
    if not ps:
        return 0.0
    H = -sum(p * math.log(p, 2) for p in ps)
    maxH = math.log(len(ps), 2) if len(ps)>1 else 1.0
    return float(H / maxH) if maxH>0 else 0.0

def build_bipartite_graph(paper_id: str, citations: List[Dict[str, Any]]) -> nx.Graph:
    """
    Build a simple bipartite graph: paper node 'P:<paper_id>' connected to field nodes 'F:<field>'.
    Also add citation nodes 'C:<citation_id>' connected to their field nodes and to paper node.
    This is a small graph used to compute centrality/bridging measures.
    """
    G = nx.Graph()
    paper_node = f"P:{paper_id}"
    G.add_node(paper_node, bipartite='paper', type='paper')
    for cit in citations:
        cid = cit.get("id") or f"C:{cit.get('title','').replace(' ','_')[:30]}"
        cit_node = f"C:{cid}"
        G.add_node(cit_node, bipartite='citation', type='citation')
        G.add_edge(paper_node, cit_node)
        for f in cit.get("fields", []):
            fn = normalize_field(f)
            fnode = f"F:{fn}"
            if not G.has_node(fnode):
                G.add_node(fnode, bipartite='field', type='field', field=fn)
            # connect citation to field
            G.add_edge(cit_node, fnode)
    return G

def compute_graph_bridge_score(G: nx.Graph, paper_id: str) -> Dict[str,float]:
    """
    Compute basic graph metrics:
      - betweenness centrality of paper node (normalized)
      - bridging coefficient (how many distinct fields it connects through citations)
    Return normalized values (0..1).
    """
    paper_node = f"P:{paper_id}"
    if paper_node not in G:
        return {"betweenness": 0.0, "field_bridge_fraction": 0.0}

    # betweenness centrality (use approximation for larger graphs in prod)
    bc = nx.betweenness_centrality(G, k=min(20, max(1, int(len(G.nodes())/2))), normalized=True)
    bet = bc.get(paper_node, 0.0)

    # how many unique field nodes reachable from paper via citations (two hops)
    neighbors = set(G.neighbors(paper_node))
    field_nodes = set()
    for n in neighbors:
        for nn in G.neighbors(n):
            if isinstance(nn, str) and nn.startswith("F:"):
                field_nodes.add(nn)
    # total distinct field nodes in graph:
    total_fields = len([n for n,d in G.nodes(data=True) if d.get('type')=='field'])
    field_bridge_fraction = 0.0
    if total_fields > 0:
        field_bridge_fraction = len(field_nodes) / total_fields
    return {"betweenness": float(min(1.0,bet)), "field_bridge_fraction": float(min(1.0, field_bridge_fraction))}

# -------------------------
# Main aggregator
# -------------------------
def compute_interdisciplinary_bridging(paper_id_or_doi: str, paper_meta: Dict[str,Any]=None,
                                      citations: List[Dict[str,Any]] = None,
                                      weights: Dict[str,float]=None) -> Dict[str,Any]:
    """
    Main entry point.
    - paper_id_or_doi: unique id used for graph node labeling (string)
    - paper_meta: optional dict with paper metadata
    - citations: optional list; if None, will call fetch_citations_with_fields()
    - weights: dict for combining components; keys: breadth(entropy), distance, graph_betweenness, field_fraction
    Returns: dictionary with components and final bridging score (0..100) plus details.
    """
    if citations is None:
        citations = fetch_citations_with_fields(paper_id_or_doi)

    # Compile field counts
    field_counts = field_counts_from_citations(citations)
    fields = list(field_counts.keys())

    # embed fields (if only one field, embedding still computed)
    field_embs = embed_fields(fields)

    # pairwise distances
    distances = compute_pairwise_field_distances(field_embs) if len(field_embs) > 0 else {}

    # component computations
    breadth = field_entropy(field_counts)  # 0..1
    pairwise_dist = weighted_mean_pairwise_distance(field_counts, distances) if distances else 0.0
    # graph-based bridging
    G = build_bipartite_graph(paper_id_or_doi, citations)
    graph_metrics = compute_graph_bridge_score(G, paper_id_or_doi)

    # default weights if not provided
    if weights is None:
        weights = {"breadth": 0.30, "distance": 0.40, "betweenness": 0.20, "field_fraction": 0.10}
    # normalize weights
    total_w = sum(weights.values()) or 1.0
    w = {k:weights[k]/total_w for k in weights}

    # Compose raw score
    raw = (breadth * w["breadth"] +
           pairwise_dist * w["distance"] +
           graph_metrics["betweenness"] * w["betweenness"] +
           graph_metrics["field_bridge_fraction"] * w["field_fraction"])

    # scale to 0..100
    bridging_score = round(max(0.0, min(1.0, raw)) * 100, 2)

    # Build readable outputs
    result = {
        "paper_id": paper_id_or_doi,
        "paper_meta": paper_meta or {},
        "n_citations": len(citations),
        "field_counts": dict(field_counts),
        "components": {
            "breadth_entropy": round(breadth, 4),
            "mean_pairwise_distance": round(pairwise_dist, 4),
            "graph_betweenness": round(graph_metrics["betweenness"], 4),
            "field_fraction_connected": round(graph_metrics["field_bridge_fraction"], 4)
        },
        "weights": w,
        "bridging_score": bridging_score,
        # extras for visualization
        "field_embeddings": {k: list(map(float,v)) for k,v in field_embs.items()},
        "pairwise_distances": {f"{a}__{b}": round(distances.get((a,b),0.0),4) for a in fields for b in fields},
        "graph_edges": list(G.edges()),
    }
    return result

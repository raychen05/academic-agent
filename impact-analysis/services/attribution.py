# attribution.py
from typing import List, Dict, Any, Optional
import math

# ------------------------------
# Attribution heuristics
# ------------------------------

def fractional_credit(n_authors: int) -> List[float]:
    """Equal fractional credit to each author."""
    return [1.0 / n_authors] * n_authors

def harmonic_credit(n_authors: int) -> List[float]:
    """Harmonic credit: author i gets 1/i normalized."""
    raw = [1.0 / (i + 1) for i in range(n_authors)]
    s = sum(raw)
    return [r / s for r in raw]

def positional_credit(n_authors: int, first_weight=0.4, last_weight=0.3) -> List[float]:
    """
    Positional credit: allocate heavier weight to first and/or last authors,
    remainder distributed evenly across middle authors.
    first_weight + last_weight must be <= 1.0
    """
    assert 0 <= first_weight <= 1 and 0 <= last_weight <= 1
    assert first_weight + last_weight <= 1.0
    if n_authors == 1:
        return [1.0]
    if n_authors == 2:
        # First and last are same as first/second
        return [first_weight, last_weight] if (first_weight + last_weight) > 0 else [0.5, 0.5]
    middle_weight_total = 1.0 - (first_weight + last_weight)
    middle_each = middle_weight_total / max(1, n_authors - 2)
    weights = []
    for i in range(n_authors):
        if i == 0:
            weights.append(first_weight)
        elif i == n_authors - 1:
            weights.append(last_weight)
        else:
            weights.append(middle_each)
    # Normalization safety
    s = sum(weights)
    return [w / s for w in weights]

# ------------------------------
# Combine heuristics and contextual signals
# ------------------------------

def apply_role_multiplier(base_weights: List[float], roles: List[str]) -> List[float]:
    """
    roles: list of roles per author e.g. ["first","coauthor","last"]
    Apply small multipliers for named roles (first, last, corresponding).
    """
    multipliers = []
    for r in roles:
        r_l = (r or "").lower()
        if "first" in r_l:
            multipliers.append(1.15)
        elif "last" in r_l or "senior" in r_l:
            multipliers.append(1.10)
        elif "corresponding" in r_l:
            multipliers.append(1.12)
        else:
            multipliers.append(1.0)
    adjusted = [w * m for w, m in zip(base_weights, multipliers)]
    s = sum(adjusted)
    return [a / s for a in adjusted]

def apply_grant_allocation(author_weights: List[float],
                           grants: Optional[List[Dict[str, Any]]],
                           author_to_grant_shares: Optional[Dict[str, Dict[str, float]]] = None
                          ) -> Dict[str, float]:
    """
    Distribute paper-level credit across grants and authors.
    - grants: list of {'grant_id':..., 'amount': optional numeric} (amount used as relative weight)
    - author_to_grant_shares: mapping author_name -> {grant_id: share} (shares sum to 1 for that author)
    Returns mapping author_name -> final_score (normalized across authors so sum=1)
    """
    # author_weights is aligned to a authors list externally; this function assumes caller will map indexes.
    # Here we only return multipliers per author (i.e. returns same-length list normalized).
    # For simplicity, if no grants provided, return normalized author_weights unchanged.
    if not grants:
        s = sum(author_weights)
        return [w / s for w in author_weights]

    # Build grant weights
    grant_weights = []
    for g in grants:
        amt = g.get("amount", 1.0)
        grant_weights.append(max(0.0, float(amt)))  # guard
    total_grant = sum(grant_weights) or 1.0
    grant_weights = [gw / total_grant for gw in grant_weights]

    # If author_to_grant_shares not provided assume uniform share across grants for each author
    n_grants = len(grants)
    final_scores = []
    for idx, base in enumerate(author_weights):
        # Try find author name mapping - but here we only accept that author_to_grant_shares is keyed by index string or name
        # Caller is responsible to pass shares keyed by author name.
        # For simplicity: assume uniform distribution across grants for each author
        shared = 0.0
        for g_w in grant_weights:
            shared += base * g_w
        final_scores.append(shared)
    # Normalize
    s = sum(final_scores) or 1.0
    return [fs / s for fs in final_scores]


# ------------------------------
# Public interface: attribute_paper
# ------------------------------

def attribute_paper(paper: Dict[str, Any],
                    method: str = "positional",
                    first_weight: float = 0.4,
                    last_weight: float = 0.3,
                    use_role_multiplier: bool = True,
                    grants: Optional[List[Dict[str, Any]]] = None,
                    author_to_grant_shares: Optional[Dict[str, Dict[str, float]]] = None
                   ) -> Dict[str, Any]:
    """
    paper: {
        "title": str,
        "authors": [ {"name": str, "affiliation": str, "role": optional str}, ... ],
        "citations": int (optional),
        "year": int (optional),
        "doi": str (optional)
    }
    method: "fractional", "harmonic", "positional"
    Returns a structured attribution result: authors with normalized shares, institutions aggregation, grant mapping.
    """
    authors = paper.get("authors", [])
    n = len(authors)
    if n == 0:
        return {"error": "no authors provided"}

    if method == "fractional":
        base = fractional_credit(n)
    elif method == "harmonic":
        base = harmonic_credit(n)
    else:
        base = positional_credit(n, first_weight=first_weight, last_weight=last_weight)

    roles = [a.get("role", "") for a in authors]
    if use_role_multiplier:
        adjusted = apply_role_multiplier(base, roles)
    else:
        adjusted = base

    # Optionally apply grant allocation distribution
    final_author_weights = apply_grant_allocation(adjusted, grants, author_to_grant_shares)

    # incorporate citation multiplier (so that more-cited papers contribute more absolute impact)
    citations = float(paper.get("citations", 0.0))
    # We'll compute both normalized shares (sum=1) and citation-weighted contributions
    s = sum(final_author_weights) or 1.0
    normalized = [w / s for w in final_author_weights]

    # citation-weighted absolute impact per author
    if citations > 0:
        abs_impact = [w * citations for w in normalized]
    else:
        abs_impact = [w for w in normalized]  # if no citations, just return normalized share

    # Institution aggregation
    inst_map = {}
    for a, w, abs_i in zip(authors, normalized, abs_impact):
        inst = a.get("affiliation", "Unknown")
        if inst not in inst_map:
            inst_map[inst] = {"share": 0.0, "absolute_impact": 0.0, "authors": []}
        inst_map[inst]["share"] += w
        inst_map[inst]["absolute_impact"] += abs_i
        inst_map[inst]["authors"].append({"name": a.get("name"), "share": w, "absolute_impact": abs_i})

    # Grants attribution (simple proportional split by grant weights)
    grant_map = {}
    if grants:
        # Normalize provided grants by amount
        total_amt = sum([g.get("amount", 1.0) for g in grants]) or 1.0
        for i, g in enumerate(grants):
            gid = g.get("grant_id", f"grant_{i}")
            grant_map[gid] = {"meta": g, "allocation": g.get("amount", 1.0) / total_amt, "authors": []}
        # Distribute author shares to grants using author_to_grant_shares if present, else proportional to grant allocation
        for a, w in zip(authors, normalized):
            name = a.get("name")
            shares = author_to_grant_shares.get(name, None) if author_to_grant_shares else None
            if shares:
                for gid, share in shares.items():
                    if gid not in grant_map:
                        continue
                    grant_map[gid]["authors"].append({"name": name, "share": w * share, "absolute_impact": (w * share) * citations})
            else:
                # distribute proportionally to grant allocation
                for gid, ginfo in grant_map.items():
                    alloc = ginfo["allocation"]
                    grant_map[gid]["authors"].append({"name": name, "share": w * alloc, "absolute_impact": (w * alloc) * citations})

    # Build author-level output
    authors_out = []
    for a, w, abs_i in zip(authors, normalized, abs_impact):
        authors_out.append({
            "name": a.get("name"),
            "affiliation": a.get("affiliation"),
            "role": a.get("role", ""),
            "share": round(w, 6),
            "absolute_impact": round(abs_i, 4)
        })

    result = {
        "paper": {"title": paper.get("title"), "doi": paper.get("doi"), "citations": citations, "year": paper.get("year")},
        "method": method,
        "authors": authors_out,
        "institutions": inst_map,
        "grants": grant_map,
        "notes": "Shares are normalized to sum=1. absolute_impact = share * citations (if citations provided)."
    }
    return result

# src/normalizer/ranking/context_features.py
def ctx_score(entity_type: str, user_ctx: dict, cand_row: dict) -> float:
    """
    Example: for organizations, boost if user_ctx.country == cand_row.country
    for journals, boost if issn matches; for funders, match country/parent org.
    Return value in [0, 1].
    """
    s = 0.0
    if entity_type == "organizations":
        if user_ctx.get("country") and cand_row.get("country"):
            s += 1.0 if user_ctx["country"] == cand_row["country"] else 0.0
    if entity_type == "journals":
        if user_ctx.get("issn") and cand_row.get("issn"):
            s += 1.0 if user_ctx["issn"] == cand_row["issn"] else 0.0
    # ... extend rules as needed
    return min(s, 1.0)

def ctx_score(entity: str, user_ctx: dict, cand_row: dict) -> float:
    s = 0.0
    if entity == "journals":
        if user_ctx.get("issn") and cand_row.get("issn"):
            s += 1.0 if user_ctx["issn"] == cand_row["issn"] else 0.0
    if entity == "organizations":
        if user_ctx.get("country") and cand_row.get("country"):
            s += 1.0 if user_ctx["country"] == cand_row["country"] else 0.0
    if entity == "funders":
        if user_ctx.get("country") and cand_row.get("country"):
            s += 1.0 if user_ctx["country"] == cand_row["country"] else 0.0
    if entity == "countries":
        if user_ctx.get("iso2") and cand_row.get("iso2"):
            s += 1.0 if user_ctx["iso2"].upper() == cand_row["iso2"].upper() else 0.0
    # topics: boost parent/children keywords overlap if you add it
    return min(s, 1.0)

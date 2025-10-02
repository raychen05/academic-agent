def build_prompt(title, abstract, top_experts):
    expert_blurbs = []
    for e in top_experts:
        expert_blurbs.append({
            "name": e["name"],
            "affiliation": e["affiliation"],
            "expertise": e["expertise"],
            "citations": e["total_citations"],
            "recent_papers": e.get("recent_papers", [])
        })

    return f"""
You are an AI assistant helping match academic experts to a research topic.
The topic is:

Title: {title}
Abstract: {abstract}

Below is a list of candidate experts:
{expert_blurbs}

For each expert, return:
- name
- affiliation
- expertise
- relevance_reason (explain why matched)
- conflict_risks (if any)
- contact (if available)

Output a JSON array of top 5-10 experts.
"""

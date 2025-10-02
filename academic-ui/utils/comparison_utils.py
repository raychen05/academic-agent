
def compare_two_papers(paper1, paper2):
    """
    Basic comparison logic – can be extended with LLM, embeddings, etc.
    """
    return {
        "Title A": paper1["title"],
        "Title B": paper2["title"],
        "Abstract Diff": diff_abstracts(paper1["abstract"], paper2["abstract"]),
        "Method Similarity": "TBD",
        "Novelty Comparison": "TBD"
    }

def diff_abstracts(abs1, abs2):
    # Placeholder for actual semantic or token diff
    return f"Abstract 1: {abs1[:200]}...\n\n---VS---\n\nAbstract 2: {abs2[:200]}..."

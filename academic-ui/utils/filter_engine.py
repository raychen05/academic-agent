
def filter_papers(papers, filters):
    def match(paper):
        # Topic cluster match
        if filters["topics"]:
            if not any(topic in paper.get("topic_clusters", []) for topic in filters["topics"]):
                return False

        # Novelty score filter
        novelty = paper.get("novelty_score", 0.0)
        if not (filters["novelty"][0] <= novelty <= filters["novelty"][1]):
            return False

        # Citation trend
        if filters["trend"] != "Any":
            if paper.get("citation_trend", "Unknown") != filters["trend"]:
                return False

        # Application domain match
        if filters["domains"]:
            if not any(domain in paper.get("application_domains", []) for domain in filters["domains"]):
                return False

        return True

    return [paper for paper in papers if match(paper)]

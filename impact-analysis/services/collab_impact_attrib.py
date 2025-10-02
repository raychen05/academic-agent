
# example_run.py
from attribution import attribute_paper
import json

def collaborator_impact_attribution():
    paper = {
        "title": "Large Language Models for Predicting Catalyst Reaction Pathways",
        "doi": "10.1000/exampledoi",
        "authors": [
            {"name": "Alice Smith", "affiliation": "Univ A", "role": "first"},
            {"name": "Bob Jones", "affiliation": "Univ B", "role": "coauthor"},
            {"name": "Carol Lee", "affiliation": "Univ A", "role": "last, senior"}
        ],
        "citations": 12,
        "year": 2022
    }

    grants = [
        {"grant_id": "G1", "amount": 500000},
        {"grant_id": "G2", "amount": 250000}
    ]

    # Optional per-author grant shares (author_name -> {grant_id: share})
    author_to_grant_shares = {
        "Alice Smith": {"G1": 0.8, "G2": 0.2},
        "Bob Jones": {"G1": 0.0, "G2": 1.0},
        "Carol Lee": {"G1": 0.5, "G2": 0.5}
    }

    res = attribute_paper(paper, method="positional", first_weight=0.45, last_weight=0.35,
                        use_role_multiplier=True, grants=grants, author_to_grant_shares=author_to_grant_shares)

    print(json.dumps(res, indent=2))

    return res

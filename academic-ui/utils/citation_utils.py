import random
import requests
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9202")  # or your ES cluster


ES_HOST = "http://localhost:9202"  # change if different
INDEX_NAME = "incites"  # your index name


def classify_citation_context(text):
    # In practice, use a fine-tuned SciBERT classifier. Here is a mock:
    keywords = {
        "support": ["builds on", "extends", "confirms"],
        "contrast": ["differs from", "disagrees", "unlike"],
        "background": ["based on", "according to", "first introduced"]
    }
    for label, phrases in keywords.items():
        if any(p in text.lower() for p in phrases):
            return label
    return random.choice(["supporting", "contrasting", "forward-looking", "contradictory", "background", "methodological", "conceptual", "observational", "empirical", "diagnostic",  "pathological", "biomarker", "mechanistic", "clinical application", "biological insight", "biological implication", "clinical relevance", "diagnostic challenge", "clinical implication", "clinical application", "future direction"])

def extract_influential_citations(citations):
    return [c for c in citations if "novel" in c["text"].lower() or "first to" in c["text"].lower()]


def get_cited_paper_ids_es(paper_id: str, max_hits=100):
    """
    Return list of UIDs/IDs of papers this paper cites.
    """
    query = {
        "query": {
            "term": {
                "isi_loc": paper_id  # assumes reverse link is indexed
            }
        },
        "_source": ["cited_docs"],
        "size": max_hits
    }

    res = es.search(index=INDEX_NAME, body=query)
    return [hit["_source"]["cited_docs"] for hit in res["hits"]["hits"]]


def get_citing_paper_ids_es(paper_id: str, max_hits=100):
    """
    Return list of UIDs/IDs of papers that cite this paper.
    """
    query = {
        "query": {
            "term": {
                "cited_docs": paper_id
            }
        },
        "_source": ["isi_loc"],
        "size": max_hits
    }

    res = es.search(index=INDEX_NAME, body=query)
    return [hit["_source"]["isi_loc"] for hit in res["hits"]["hits"]]



def get_cited_paper_ids(paper_id: str, max_hits=100):
    """
    Return list of UIDs/IDs of papers this paper cites using raw REST API.
    """
    url = f"{ES_HOST}/{INDEX_NAME}/_search"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    query = {
        "query": {
            "term": {
                "isi_loc": paper_id  # assumes reverse link is indexed
            }
        },
        "_source": ["cited_docs"],
        "size": max_hits
    }

    response = requests.post(url, headers=headers, json=query)

    if response.status_code != 200:
        raise RuntimeError(f"Elasticsearch query failed: {response.text}")

    res = response.json()
    return [hit["_source"]["cited_docs"] for hit in res["hits"]["hits"] if "cited_docs" in hit["_source"]]


def get_citing_paper_ids(paper_id: str, max_hits=100):
    """
    Return list of UIDs/IDs of papers that cite the given paper using REST API.
    """
    url = f"{ES_HOST}/{INDEX_NAME}/_search"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    query = {
        "query": {
            "term": {
                "cited_docs": paper_id
            }
        },
        "_source": ["isi_loc"],
        "size": max_hits
    }

    response = requests.post(url, headers=headers, json=query)

    if response.status_code != 200:
        raise RuntimeError(f"Elasticsearch query failed: {response.text}")

    res = response.json()
    return [hit["_source"]["isi_loc"] for hit in res["hits"]["hits"] if "isi_loc" in hit["_source"]]



def get_citing_papers(paper_id: str, max_hits=20):
    """
    Return list of UIDs/IDs of papers that cite the given paper using REST API.
    """
    url = f"{ES_HOST}/{INDEX_NAME}/_search"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    query = {
        "query": {
            "term": {
                "cited_docs": paper_id
            }
        },
        "_source": ["isi_loc"],
        "size": max_hits
    }

    response = requests.post(url, headers=headers, json=query)

    if response.status_code != 200:
        raise RuntimeError(f"Elasticsearch query failed: {response.text}")

    res = response.json()
    return [hit["_source"]["isi_loc"] for hit in res["hits"]["hits"] if "isi_loc" in hit["_source"]]

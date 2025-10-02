from typing import List
from short_term import get_messages
from vector_store import search as vector_search
from kg import query_related
from summarizer import summarize_chunk

# simple hierarchical retrieval policy
async def retrieve_context(conv_id: str, query: str):
    # 1) short-term
    st = get_messages(conv_id)
    # naive relevance filtering: include messages that contain tokens from query
    st_filtered = [m for m in st if any(tok.lower() in m['content'].lower() for tok in query.split()[:5])]

    # 2) summaries (not implemented as persistence in prototype) - placeholder
    
    # 3) vector DB
    vd = vector_search(query, top_k=5)

    # 4) KG
    kg = query_related(query.split()[0]) if query.split() else []

    # assemble
    assembled = {
        "short_term": st_filtered,
        "vector_hits": vd,
        "kg": kg,
    }
    return assembled
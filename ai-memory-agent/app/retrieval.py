from memory_manager import retrieve_context
from summarizer import summarize_chunk

async def retrieval_pipeline(conv_id: str, query: str):
    ctx = await retrieve_context(conv_id, query)
    # produce a compact prompt: prefer summaries + top vector hits + short-term
    prompt_parts = []
    if ctx['short_term']:
        prompt_parts.append("Recent:")
        for m in ctx['short_term'][-10:]:
            prompt_parts.append(f"{m['role']}: {m['content']}")
    # vector hits payload -> include payload text if available
    if ctx['vector_hits']:
        prompt_parts.append("Relevant past memories:")
        for hit in ctx['vector_hits']:
            # qdrant returns payload in .payload
            txt = hit.payload.get('text') if hasattr(hit, 'payload') else hit.payload
            prompt_parts.append(str(txt))
    if ctx['kg']:
        prompt_parts.append("Related facts:")
        prompt_parts.extend([str(x) for x in ctx['kg']])

    final_prompt = "\n".join(prompt_parts)
    return final_prompt


from fastapi import HTTPException
from short_term import add_message
from retrieval import retrieval_pipeline
from summarizer import call_llm

async def handle_user_message(conv_id: str, role: str, content: str):
    # ingest
    add_message(conv_id, role, content)
    # retrieve context
    prompt = await retrieval_pipeline(conv_id, content)
    # assemble system message
    system = "You are an assistant. Use context below when responding."
    assembled = f"{system}\n\nContext:\n{prompt}\n\nUser: {content}\n\nAssistant:"
    # call LLM
    resp = await call_llm(assembled)
    return resp
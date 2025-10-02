# Minimal LLM wrapper for summarization. Replace with your LLM or OpenAI calls.
import httpx
from typing import List
from config import settings

async def call_llm(prompt: str) -> str:
    # placeholder: call your LLM here (OpenAI or local model)
    # For demo we'll just return the first 300 chars as a naive 'summary'.
    return prompt[:300]

async def summarize_chunk(messages: List[dict]) -> dict:
    text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    summary = await call_llm(f"Summarize the following conversation:\n\n{text}\n\nKey bullets:")
    return {"summary": summary, "range": (messages[0]['ts'], messages[-1]['ts'])}
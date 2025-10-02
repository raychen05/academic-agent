# tools/co_writer.py

import os
from openai import OpenAI

class CoWriter:
    def __init__(self):
        # Load OpenAI API key from env
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_answer_stub(self, query, context_chunks):
        """
        Combine query + retrieved chunks into a final answer.
        """
        context = "\n".join(context_chunks)
        return f"Answer for '{query}':\n{context}\n[This is a stub answer.]"
    

    def generate_answer(self, query: str, context_chunks: list) -> str:
        """
        Combine user query and retrieved chunks, and generate an answer using an LLM.
        """

        # Join context chunks into a single prompt
        context_text = "\n\n".join(
            f"Context {i+1}:\n{chunk}" for i, chunk in enumerate(context_chunks)
        )

        # Build the system & user messages
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful academic research assistant. "
                    "Use the provided context to answer the question clearly and concisely. "
                    "If the context is insufficient, say you don't know."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n{context_text}\n\n"
                    f"Question: {query}"
                )
            }
        ]

        # Call the OpenAI Chat Completion API
        response = self.client.chat.completions.create(
            model="gpt-4o",  # Use your preferred model
            messages=messages,
            temperature=0.2
        )

        answer = response.choices[0].message.content
        return answer


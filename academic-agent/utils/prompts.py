# utils/prompts.py

classify_prompt = """
Classify this query into one of: [fact, review, opinion].

Query: "{query}"
Answer:"""

reformulate_prompt = """
Reformulate this research query to make it more effective for academic search engines:

Original: "{query}"
Rewritten:"""

generate_prompt = """
Use the following documents to answer the research question.

Question: {query}

Documents:
{context}

Answer:"""
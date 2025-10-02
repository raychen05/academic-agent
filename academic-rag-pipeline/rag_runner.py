from rag_config import load_and_chunk_docs, build_vectorstore
from structured_prompt import rag_chain

def run_rag_pipeline(file_path: str, user_query: str):
    print("📄 Loading and chunking document...")
    docs = load_and_chunk_docs(file_path)
    
    print("🧠 Building vector store...")
    vs = build_vectorstore(docs)

    print("🔍 Performing semantic search...")
    results = vs.similarity_search(user_query, k=3)
    context = "\n\n".join([doc.page_content for doc in results])

    print("📝 Running LLM for structured summary...")
    structured_output = rag_chain.run({"context": context})

    return structured_output

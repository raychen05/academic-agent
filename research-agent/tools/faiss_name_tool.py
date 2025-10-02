
# LangChain Tool Wrapper

from langchain.tools import Tool
from matching.faiss_matcher import FAISSNameMatcher

# Load once at init
matcher = FAISSNameMatcher(
    index_path="data/author_embeddings.npy",
    name_list_path="data/author_names.json"
)

def faiss_name_match_tool(query: str) -> str:
    results = matcher.match(query, k=5)
    output = "\n".join([f"{r['name']} (distance: {r['score']:.4f})" for r in results])
    return f"Top canonical name matches for '{query}':\n" + output

faiss_match_tool = Tool(
    name="NameMatcherFAISS",
    func=faiss_name_match_tool,
    description="Use this to match a messy author, institution, or funder name to the best canonical names using embeddings."
)



from langchain.tools import tool
import requests
import os

INCITES_API_KEY = os.getenv("WOS_API_KEY")

@tool
def incites_tool(query: str) -> str:
    """Search Web of Science for recent papers on a topic."""
    url = f"https://api.clarivate.com/incites?query={query}&apikey={INCITES_API_KEY}"
    res = requests.get(url)
    return res.text[:1000]  # Simplified return

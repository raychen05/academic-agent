

from langchain.tools import tool
import requests
import os

WOS_API_KEY = os.getenv("WOS_API_KEY")

@tool
def wos_tool(query: str) -> str:
    """Search Web of Science for recent papers on a topic."""
    url = f"https://api.clarivate.com/wos?query={query}&apikey={WOS_API_KEY}"
    res = requests.get(url)
    return res.text[:1000]  # Simplified return



#  Define Your Nodes (Functions per step)

from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from tools import wos_tool, incites_tool, vector_search_tool

def parse_intent(state):
    query = state['input']
    if "funding" in query.lower():
        return "use_incites"
    elif "novelty" in query.lower():
        return "use_vector"
    else:
        return "use_wos"

def use_wos(state):
    return {"result": wos_tool(state['input'])}

def use_incites(state):
    return {"result": incites_tool(state['input'])}

def use_vector(state):
    return {"result": vector_search_tool(state['input'])}
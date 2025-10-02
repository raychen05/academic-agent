
#  Build the LangGraph

from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from nodes import parse_intent, use_wos, use_incites, use_vector

# Create graph
graph = StateGraph()

# Add nodes
graph.add_node("router", RunnableLambda(parse_intent))
graph.add_node("use_wos", RunnableLambda(use_wos))
graph.add_node("use_incites", RunnableLambda(use_incites))
graph.add_node("use_vector", RunnableLambda(use_vector))

# Routing logic
graph.set_entry_point("router")
graph.add_conditional_edges("router", {
    "use_wos": "use_wos",
    "use_incites": "use_incites",
    "use_vector": "use_vector"
})

# End all nodes
graph.set_finish_point("use_wos")
graph.set_finish_point("use_incites")
graph.set_finish_point("use_vector")

# Compile
graph_app = graph.compile()
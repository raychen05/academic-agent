
from fastapi import FastAPI
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from agent.memory import get_memory

from tools.wos_tool import wos_tool
from tools.incites_tool import incites_tool
from tools.vector_search_tool import vector_search_tool
from tools.faiss_name_tool import faiss_name_match_tool


llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Register tools
tools = [wos_tool, incites_tool, vector_search_tool, faiss_name_match_tool]

# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


# Initialize agent with tools and memory
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    memory=get_memory(),
    verbose=True
)

# FastAPI service
app = FastAPI()

@app.get("/ask")
def ask(query: str):
    result = agent.run(query)
    return {"result": result}


# Use LangGraph for more complex routing
@app.get("/research_agent")
def run_agent(query: str):
    result = graph_app.invoke({"input": query})
    return {"result": result["result"]}



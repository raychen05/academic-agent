# run_api.py
from fastapi import FastAPI
from pydantic import BaseModel
from agent.planner import Planner

app = FastAPI(title="ResearchCompass API")

planner = Planner()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_ai(request: QueryRequest):
    """
    接收一个研究问题，调用多步骤推理
    """
    state = {}  # TODO: 调用 AgentState
    result = planner.plan_steps(state)
    return {"answer": result or "这是占位答案，Planner 还没实现完整逻辑"}
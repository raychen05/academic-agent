from fastapi import FastAPI
from orchestrator import handle_user_message
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    conv_id: str
    role: str
    content: str

@app.post('/message')
async def message(msg: Message):
    res = await handle_user_message(msg.conv_id, msg.role, msg.content)
    return {"answer": res}
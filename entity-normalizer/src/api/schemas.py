# src/api/schemas.py
from pydantic import BaseModel
class NormalizeReq(BaseModel):
    entity_type: str
    text: str
    context: dict | None = None

class NormalizeResp(BaseModel):
    id: str | None
    name: str | None
    score: float

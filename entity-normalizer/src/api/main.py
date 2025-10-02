# src/api/main.py
from fastapi import FastAPI
from .schemas import NormalizeReq, NormalizeResp
from ..normalizer.pipeline import NormalizationPipeline

app = FastAPI(title="Local Entity Normalizer")
pipe = NormalizationPipeline()

@app.post("/normalize", response_model=NormalizeResp)
def normalize(req: NormalizeReq):
    out = pipe.normalize(req.entity_type, req.text, req.context)
    return NormalizeResp(id=out.get("id"), name=out.get("name"), score=out.get("score", 0.0))


### Example usage:
### uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
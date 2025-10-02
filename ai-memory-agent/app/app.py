from fastapi import FastAPI, Query
from pydantic import BaseModel
import os
import redis
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from neo4j import GraphDatabase
from dotenv import load_dotenv
import uuid

load_dotenv()

app = FastAPI(title="AI Memory Agent API")

# --- Redis ---
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

# --- Qdrant ---
qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))

# --- Neo4j ---
neo4j_driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    auth=(
        os.getenv("NEO4J_USER", "neo4j"),
        os.getenv("NEO4J_PASSWORD", "password")
    )
)

# ---------------------------
# Redis Endpoints
# ---------------------------

class RedisSetRequest(BaseModel):
    key: str
    value: str

@app.post("/redis/set")
def redis_set(data: RedisSetRequest):
    redis_client.set(data.key, data.value)
    return {"status": "ok", "key": data.key}

@app.get("/redis/get")
def redis_get(key: str):
    value = redis_client.get(key)
    return {"key": key, "value": value}

@app.get("/redis/keys")
def redis_keys(pattern: str = "*"):
    keys = redis_client.keys(pattern)
    return {"keys": keys}

# ---------------------------
# Qdrant Endpoints
# ---------------------------

class QdrantInsertRequest(BaseModel):
    collection_name: str
    vector: list[float]
    payload: dict

class QdrantScrollRequest(BaseModel):
    collection_name: str
    limit: int

@app.post("/qdrant/insert")
def qdrant_insert(data: QdrantInsertRequest):
    point_id = str(uuid.uuid4())
    qdrant_client.upsert(
        collection_name=data.collection_name,
        points=[
            PointStruct(
                id=point_id,
                vector=data.vector,
                payload=data.payload
            )
        ]
    )
    return {"status": "ok", "id": point_id}

@app.get("/qdrant/scroll")
def qdrant_scroll(collection_name: str, limit: int = 5):
    res = qdrant_client.scroll(collection_name=collection_name, limit=limit)
    return {"points": res[0]}


@app.get("/qdrant/scroll2")
def qdrant_scroll(data: QdrantScrollRequest):
    res = qdrant_client.scroll(collection_name=data.collection_name, limit=data.limit)
    return {"points": res[0]}

# ---------------------------
# Neo4j Endpoints
# ---------------------------

class Neo4jQueryRequest(BaseModel):
    cypher: str

@app.post("/neo4j/query")
def neo4j_query(data: Neo4jQueryRequest):
    with neo4j_driver.session() as session:
        result = session.run(data.cypher)
        records = [dict(record) for record in result]
    return {"records": records}

@app.get("/neo4j/nodes")
def neo4j_get_nodes():
    with neo4j_driver.session() as session:
        result = session.run("MATCH (n) RETURN n LIMIT 5")
        records = [dict(record["n"]) for record in result]
    return {"nodes": records}

class Neo4jNodeRequest(BaseModel):
    label: str
    properties: dict

@app.post("/neo4j/create-node")
def neo4j_create_node(data: Neo4jNodeRequest):
    with neo4j_driver.session() as session:
        cypher = f"CREATE (n:{data.label} $props) RETURN n"
        result = session.run(cypher, props=data.properties)
        return {"node": [dict(record["n"]) for record in result]}



# ---------------------------
# Health Check
# ---------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

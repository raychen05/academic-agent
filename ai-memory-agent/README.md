### Setup and Run Instructions for Starter Repo (Python + Redis + Qdrant + Neo4j)

#### 1. Clone the Repository
   
```bash
git clone https://github.com/yourusername/ai-memory-agent.git
cd ai-memory-agent
```


#### 2. Install Dependencies

We recommend using Python 3.10+

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Example requirements.txt:
```text
redis
qdrant-client
neo4j
openai
```

#### 3. Start Required Services

Make sure you have Docker installed, then run:

```bash
docker run -d --name redis -p 6379:6379 redis:latest
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant:latest
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
```

#### 4. Configure Environment Variables

Create a .env file in the project root:

```text
OPENAI_API_KEY=your_openai_key_here
QDRANT_URL=http://localhost:6333
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
REDIS_HOST=localhost
REDIS_PORT=6379
```


#### 5. Initialize Qdrant Collection

Run the following snippet once to create the collection:
```bash
python scripts/init_qdrant.py
```


#### 6. Run the Summarizer Example

```bash
python examples/run_summarizer.py
```

This will:

- Connect to Redis, Qdrant, Neo4j
- Load sample conversation messages
- Generate a summary with embeddings
- Store it in Qdrant with provenance metadata


#### 7. Query Summaries

Use scripts/query_qdrant.py to search summaries by semantic similarity.


**Tip**: You can extend the Summarizer class to automatically trigger when Redis' short-term buffer reaches a limit, ensuring summaries are persisted with provenance.


#### 8. Check Data in Each Service

Redis

```python
import redis
r = redis.Redis(host='localhost', port=6379)
print(r.keys())  # List all keys
print(r.get('some_key'))  # Get value of a specific key
```

Qdrant

```python
from qdrant_client import QdrantClient
client = QdrantClient(url="http://localhost:6333")
res = client.scroll(collection_name="summaries", limit=5)
print(res)
```

Neo4j

```python

from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
with driver.session() as session:
    result = session.run("MATCH (n) RETURN n LIMIT 5")
    for record in result:
        print(record)
```

#### 9. Check Data via REST Calls


Redis (keys & values)

```bash
curl localhost:6379   # Redis doesn't use HTTP, use redis-cli instead
redis-cli -h localhost -p 6379 keys '*'
redis-cli -h localhost -p 6379 get msg:0
```

Qdrant (list points)

```bash
curl -X POST "http://localhost:6333/collections/summaries/points/scroll" \
  -H 'Content-Type: application/json' \
  -d '{"limit":5}'
```

Neo4j (query nodes via HTTP API)

```bash
curl -u neo4j:password -H 'Content-Type: application/json' \
  -d '{"statements":[{"statement":"MATCH (n) RETURN n LIMIT 5"}]}' \
  http://localhost:7474/db/neo4j/tx/commit
```

Summary:
Neo4j queries go to /db/{dbName}/tx/commit endpoint.
/collections/summaries/points/scroll is not Neo4j REST API — so Neo4j auth and Cypher query won’t work.


10. Run FAST API Locally


- To run MainI Service. - Receive message and memorize

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001

```

URL: http://127.0.0.1:8001


- To run API Service -- REST API call wrapper

```bash
cd /Users/r.chen/workspace/academic-agent/ai-memory-agent/app
uvicorn app:app --reload
```

URL: http://127.0.0.1:8000


- To run chat UI

```bash
streamlit run chat_app.py
```

URL: http://127.0.0.1:8002

http://localhost:8501/

- To create random vector for test

```bash
python tests/gen_vect.py
```

### Set up Runtime Environment

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```


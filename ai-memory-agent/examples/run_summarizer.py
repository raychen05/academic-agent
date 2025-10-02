import os
import redis
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from openai import OpenAI
from dotenv import load_dotenv
import uuid
from app.llm_helpers import call_llm

load_dotenv()

# Setup clients
r = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")))
qdrant = QdrantClient(url=os.getenv("QDRANT_URL"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Sample conversation
messages = [
    "User: How's the weather today?",
    "Assistant: It's sunny and 25°C.",
    "User: Great, I might go hiking.",
]

# Store in Redis short-term memory
for idx, msg in enumerate(messages):
    r.set(f"msg:{idx}", msg)

# Summarize
summary_prompt = "Summarize the following conversation:\n" + "\n".join(messages)

# summary_resp = openai_client.chat.completions.create(
#    model="gpt-3.5-turbo",
#    messages=[{"role": "user", "content": summary_prompt}]
# )
# summary_text = summary_resp.choices[0].message.content.strip()
#
summary_text = call_llm(summary_prompt)  # Call LLM to process the summary

# Embed summary
# embed_resp = openai_client.embeddings.create(
#    model="text-embedding-ada-002",
#    input=summary_text
#)
# embedding_vector = embed_resp.data[0].embedding
embedding_vector = 

# Store in Qdrant with provenance
point_id = str(uuid.uuid4())
qdrant.upsert(
    collection_name="summaries",
    points=[
        PointStruct(
            id=point_id,
            vector=embedding_vector,
            payload={
                "summary": summary_text,
                "source_keys": [f"msg:{i}" for i in range(len(messages))]
            }
        )
    ]
)
print(f"Stored summary in Qdrant: {summary_text}")
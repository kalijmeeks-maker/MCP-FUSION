import os
import json
import numpy as np
from openai import OpenAI

EMBED_MODEL = "text-embedding-3-large"
MEMORY_PATH = "/Users/kalimeeks/MCP-FUSION/workspace/memory/memory.json"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ensure_memory_file():
    if not os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "w") as f:
            json.dump({"entries": []}, f)

def embed(text: str):
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=text
    )
    return np.array(response.data[0].embedding, dtype=np.float32).tolist()

def save_memory(text: str, source: str, metadata=None):
    ensure_memory_file()
    with open(MEMORY_PATH, "r") as f:
        db = json.load(f)

    embedding = embed(text)
    metadata = metadata or {}

    entry = {
        "text": text,
        "source": source,
        "embedding": embedding,
        "metadata": metadata
    }

    db["entries"].append(entry)

    with open(MEMORY_PATH, "w") as f:
        json.dump(db, f, indent=2)

def search_memory(query: str, limit: int = 5):
    ensure_memory_file()
    with open(MEMORY_PATH, "r") as f:
        db = json.load(f)

    if not db["entries"]:
        return []

    q_embed = np.array(embed(query))

    scored = []
    for e in db["entries"]:
        e_embed = np.array(e["embedding"])
        score = np.dot(q_embed, e_embed) / (np.linalg.norm(q_embed) * np.linalg.norm(e_embed))
        scored.append((score, e))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [e for _, e in scored[:limit]]

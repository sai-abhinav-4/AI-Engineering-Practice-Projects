"""
NotesGpt - A RAG chatbot over your own notes.

Architecture:
  [ you ] --> app (FastAPI, this file) --> chroma (vector DB, separate container)
                     |
                     +--> Groq API (chat completion) + Local Embeddings (all-MiniLM-L6-v2)
"""
import os
import sys
import time

import chromadb
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

# Disable Chroma telemetry warning
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Load environment variables (from local .env or project root .env)
load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    parent_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
    if os.path.exists(parent_env):
        load_dotenv(parent_env)

app = FastAPI(title="NotesGpt", description="RAG over your course notes")

# --- Fail loudly and clearly if the API key is missing ---------------------
API_KEY = os.getenv("GROQ_API_KEY", "").strip()
if not API_KEY or API_KEY.startswith("gsk_paste"):
    sys.exit(
        "\n[NotesGpt] GROQ_API_KEY is missing.\n"
        "  Fix: cp .env.example .env, put your real key in it, then\n"
        "       docker compose up -d --force-recreate\n"
    )

# Groq OpenAI-compatible LLM client
llm = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

# Local embedding model (all-MiniLM-L6-v2) - runs locally, no API key needed
print("[NotesGpt] Loading local embedding model (all-MiniLM-L6-v2)...", flush=True)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))


def connect_to_chroma(retries: int = 30, delay: int = 2):
    """
    Chroma's container takes a few seconds to boot. `depends_on` only waits for
    the container to START, not to be READY - so we retry here instead of
    crashing on the first refused connection.
    """
    for attempt in range(1, retries + 1):
        try:
            client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
            client.heartbeat()
            print(f"[NotesGpt] Connected to chroma at {CHROMA_HOST}:{CHROMA_PORT}")
            return client
        except Exception as e:
            print(
                f"[NotesGpt] Waiting for chroma "
                f"({attempt}/{retries}): {type(e).__name__}",
                flush=True,
            )
            time.sleep(delay)
    sys.exit(f"\n[NotesGpt] Could not reach chroma at {CHROMA_HOST}:{CHROMA_PORT}\n")


chroma = connect_to_chroma()
collection = chroma.get_or_create_collection(name="notes")


class Question(BaseModel):
    query: str


@app.get("/")
def health():
    return {
        "status": "NotesGpt is live 📚",
        "docs_indexed": collection.count(),
        "chroma_host": CHROMA_HOST,
        "chroma_port": CHROMA_PORT,
    }


@app.post("/ask")
def ask(q: Question):
    if collection.count() == 0:
        raise HTTPException(
            status_code=400,
            detail="No documents indexed yet. Run: docker compose exec app python ingest.py",
        )

    # 1. RETRIEVE - embed query locally and find the most relevant chunks from Chroma
    q_embedding = embedder.encode([q.query]).tolist()
    hits = collection.query(query_embeddings=q_embedding, n_results=3)
    documents = hits.get("documents") or [[]]
    context = "\n\n---\n\n".join(documents[0])

    # 2. AUGMENT - stuff that context into the prompt
    system_prompt = (
        "You are NotesGpt, a helpful teaching assistant. "
        "Answer the user's question using ONLY the context below. "
        "If the context does not contain the answer, say you don't know.\n\n"
        f"CONTEXT:\n{context}"
    )

    # 3. GENERATE - let the LLM write the final answer
    resp = llm.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": q.query},
        ],
    )

    return {
        "question": q.query,
        "answer": resp.choices[0].message.content,
        "sources_used": len(documents[0]),
    }

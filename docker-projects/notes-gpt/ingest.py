"""
Loads every .txt and .md file from docs/ into the Chroma vector database.

Run this AFTER the containers are up:
    docker compose exec app python ingest.py
"""
import glob
import os
import sys
import time

import chromadb
from sentence_transformers import SentenceTransformer

# Disable Chroma telemetry warning
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Local embedding model (all-MiniLM-L6-v2) - runs locally, no API key needed
print("[ingest] Loading local embedding model (all-MiniLM-L6-v2)...", flush=True)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

host = os.getenv("CHROMA_HOST", "localhost")
port = int(os.getenv("CHROMA_PORT", "8000"))

chroma = None
for attempt in range(10):
    try:
        chroma = chromadb.HttpClient(host=host, port=port)
        chroma.heartbeat()
        break
    except Exception:
        print(f"[ingest] waiting for chroma ({attempt + 1}/10)...", flush=True)
        time.sleep(2)
if chroma is None:
    sys.exit(f"[ingest] Could not reach chroma at {host}:{port}")

collection = chroma.get_or_create_collection(name="notes")

files = sorted(glob.glob("docs/*.txt") + glob.glob("docs/*.md"))
if not files:
    sys.exit("No files found in docs/ — add some .txt or .md notes first.")

ids, documents, metadatas = [], [], []
for path in files:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    # Simple chunking: split on blank lines, keep chunks of reasonable size
    chunks = [c.strip() for c in text.split("\n\n") if len(c.strip()) > 40]

    for i, chunk in enumerate(chunks):
        ids.append(f"{os.path.basename(path)}::{i}")
        documents.append(chunk)
        metadatas.append({"source": os.path.basename(path)})

if not documents:
    sys.exit("Files found but no usable chunks. Make paragraphs a bit longer.")

print(f"[ingest] Generating embeddings for {len(documents)} chunks...", flush=True)
embeddings = embedder.encode(documents).tolist()

# upsert with explicitly computed embeddings
collection.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

print(f"Ingested {len(documents)} chunks from {len(files)} file(s) ✅")
print(f"Collection now holds {collection.count()} chunks total.")

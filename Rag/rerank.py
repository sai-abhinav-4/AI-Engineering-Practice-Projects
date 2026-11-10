import os
import sys
from dotenv import load_dotenv

# Ensure parent directory is in sys.path to find .env and chroma_db
PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PARENT_DIR)

load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from sentence_transformers import CrossEncoder

CHROMA_PATH = os.path.join(PARENT_DIR, "chroma_db") if os.path.exists(os.path.join(PARENT_DIR, "chroma_db")) else "./chroma_db"

embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedder)

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")   # free, fast

def retrieve_with_rerank(question, top_k=3):
    candidates = db.similarity_search(question, k=25)        # grab 25 cheap candidates
    pairs = [(question, c.page_content) for c in candidates]
    scores = reranker.predict(pairs)                          # cross-encoder scores each pair
    return [c for _, c in sorted(zip(scores, candidates), reverse=True)[:top_k]]

if __name__ == "__main__":
    query = "How long do I have to return something?"
    print(f"Query: {query}\n")
    results = retrieve_with_rerank(query, top_k=3)
    for i, doc in enumerate(results, start=1):
        print(f"Rank {i}:")
        print(doc.page_content)
        print("-" * 50)

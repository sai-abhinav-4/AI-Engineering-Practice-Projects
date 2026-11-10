import os
import sys
from dotenv import load_dotenv

# Ensure parent directory is in sys.path to find .env and chroma_db
PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PARENT_DIR)

load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# ⑤ open the same vector store we built in step 1
CHROMA_PATH = os.path.join(PARENT_DIR, "chroma_db") if os.path.exists(os.path.join(PARENT_DIR, "chroma_db")) else "./chroma_db"

embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedder)

# Groq OpenAI-compatible model wrapper
model = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    temperature=0,
)

# ⑥ the prompt: instructions + chunks + question
prompt = ChatPromptTemplate.from_template("""
Answer the question using ONLY the context below. If the context doesn't contain
the answer, say "I don't know." Be concise and quote facts directly.

Context:
{context}

Question: {question}
""")


def rag_answer(question):
    chunks = db.similarity_search(question, k=3)         # ⑦ retrieve top 3
    context = "\n\n".join(c.page_content for c in chunks)
    chain = prompt | model                                # ⑧ same chain trick as Class 2
    return chain.invoke({"context": context, "question": question}).content


if __name__ == "__main__":
    print("Q: How long do I have to return something?")
    print("A:", rag_answer("How long do I have to return something?"))
    print("\nQ: What is the address of the office?")
    print("A:", rag_answer("What is the address of the office?"))
    print("\nQ: what is the office timings?")
    print("A:", rag_answer("what is the office timings?"))
    print("\nQ: what is the source of contact for corporate orders?")
    print("A:", rag_answer("what is the source of contact for corporate orders?"))
    print("\nQ: What is the capital of France?")
    print("A:", rag_answer("What is the capital of France?"))

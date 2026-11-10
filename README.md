# AI Engineering Practice Projects

This repository contains hands-on practice projects 

## First Class: LLM API Fundamentals & Applications

### 1. `first_call.py`
- Basic setup demonstrating how to connect to an LLM provider (Groq) using the OpenAI Python SDK.
- Demonstrates loading API keys securely from `.env` via `python-dotenv`.
- Executes a system + user chat completion.

### 2. `interactive_chat.py`
- Real-time streaming CLI chat application.
- Demonstrates token streaming using `stream=True` for low-latency output.
- Implements conversation memory by appending `user` and `assistant` turns into the `messages` history.

### 3. `scraper.py`
- Web scraping utility using `requests` and `BeautifulSoup4`.
- Sanitizes incoming web pages by removing clutter tags (`script`, `style`, `nav`, `footer`, `header`, `img`, `input`).
- Extracts and cleans the text to prepare it as context for LLM ingestion.

### 4. `summarizer.py`
- End-to-end AI Website Summarizer with a web UI built using **Gradio**.
- Takes a target URL from the user, uses `scraper.py` to extract page content, and prompts Groq (`openai/gpt-oss-20b`) to generate a friendly Markdown summary.
- Generates a local and shareable public link (`share=True`).

### 5. `structured_output.py`
- Enforces strict JSON output using `response_format={"type": "json_object"}`.
- Parses and validates output into a strongly-typed **Pydantic** model (`TravelPlan`).
- Inspects token usage metrics (`prompt_tokens`, `completion_tokens`, `total_tokens`).

### 6. `langchain/summarizer_langchain.py`
- Implements a LangChain Expression Language (LCEL) pipeline: `prompt | model | parser`.
- Demonstrates using LangChain's `ChatOpenAI` as a wrapper pointing to Groq's API (`base_url="https://api.groq.com/openai/v1"`).
- Fetches and sanitizes website content via `scraper.py` before passing it to the chain.

### 7. `langchain/memory_demo.py` & `langchain/memory_chat.py`
- **`memory_demo.py`**: Explains how LLMs achieve memory by re-sending past turns using LangChain's `MessagesPlaceholder("history")`.
- **`memory_chat.py`**: Interactive CLI chat that dynamically appends `HumanMessage` and `AIMessage` to the conversation history after each turn.

### 8. `langchain/first_agent.py`
- Builds a tool-calling AI Agent using Groq (`openai/gpt-oss-20b`).
- Equips the LLM with a Python tool function (`get_price`).
- Implements an autonomous decision loop: LLM decides whether to invoke the tool, extracts arguments, executes the local Python function, and returns the grounded answer.

### 9. `langchain/smart_shop_assistant.py`
- Interactive web chat interface built using **Gradio** (`gr.ChatInterface`).
- Wraps `first_agent.py` into a user-friendly shopping assistant interface with both local and shareable public links (`share=True`).

### 10. `langchain/agent_single_tool.py`
- Implements LangChain V1 `create_agent` with a custom Python tool function (`get_weather`).
- Connects to Groq using the `ChatOpenAI` provider wrapper.
- Demonstrates tool calling introspection, step-by-step tool results, and final answer generation.

### 11. `langchain/agent_multi_tools.py`
- Extends the LangChain agent with multiple specialized tools: `get_weather`, `add`, `multiply`, and `get_population`.
- Demonstrates autonomous tool selection, multi-tool execution in a single prompt, and step-by-step execution traces.

---

## Retrieval-Augmented Generation (RAG)

### 12. `Rag/embeddings.py`
- Generates 384-dimensional dense vector embeddings using `sentence-transformers` (`all-MiniLM-L6-v2`).
- Measures semantic similarity between sentences using cosine similarity (`numpy.dot` / `numpy.linalg.norm`).

### 13. `Rag/chunk.py`
- Implements document chunking using `langchain_text_splitters.RecursiveCharacterTextSplitter`.
- Splits a structured document into overlapping chunks (`chunk_size=80`, `chunk_overlap=10`) to preserve context across boundaries.

### 14. `Rag/index.py`
- Indexes documents into a persistent vector store using `langchain_chroma.Chroma`.
- Uses `langchain_huggingface.HuggingFaceEmbeddings` with `all-MiniLM-L6-v2` for local, fast vector embeddings.
- Persists vector embeddings and metadata to disk (`./chroma_db`).

---

## Setup & Running

### 1. Clone the repository
```bash
git clone https://github.com/sai-abhinav-4/AI-Engineering-Practice-Projects.git
cd AI-Engineering-Practice-Projects
```

### 2. Set up and Activate Virtual Environment (`.venv`)
Create and activate an isolated Python environment:

- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

> *Tip: Once activated, your terminal prompt will be prefixed with `(.venv)`.*

### 3. Install dependencies
With the virtual environment activated:
```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables
Copy `.env.example` to `.env` and add your Groq API key:
```powershell
copy .env.example .env
```
Inside `.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
```

---

### 5. Running Each Project (Ensure `.venv` is activated)

- **1. Basic LLM Call**
  ```powershell
  python first_call.py
  ```

- **2. Interactive CLI Chat (Streaming & Memory)**
  ```powershell
  python interactive_chat.py
  ```

- **3. AI Website Summarizer (Web UI with Gradio)**
  ```powershell
  python summarizer.py
  ```

- **4. Structured JSON Output with Pydantic**
  ```powershell
  python structured_output.py
  ```

- **5. LangChain LCEL Summarizer**
  ```powershell
  python langchain/summarizer_langchain.py
  ```

- **6. LangChain Memory Demo & Chat**
  ```powershell
  python langchain/memory_demo.py
  python langchain/memory_chat.py
  ```

- **7. Tool-Calling Agent**
  ```powershell
  python langchain/first_agent.py
  ```

- **8. Smart Shop Assistant (Web UI with Memory)**
  ```powershell
  python langchain/smart_shop_assistant.py
  ```

- **9. LangChain Single-Tool Agent**
  ```powershell
  python langchain/agent_single_tool.py
  ```

- **10. LangChain Multi-Tool Agent**
  ```powershell
  python langchain/agent_multi_tools.py
  ```

- **11. Vector Embeddings & Cosine Similarity**
  ```powershell
  python Rag/embeddings.py
  ```

- **12. Document Chunking with Overlap**
  ```powershell
  python Rag/chunk.py
  ```

- **13. Vector Indexing with ChromaDB**
  ```powershell
  python Rag/index.py
  ```

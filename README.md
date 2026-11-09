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

---

## Setup & Running

### 1. Clone the repository
```bash
git clone https://github.com/sai-abhinav-4/AI-Engineering-Practice-Projects.git
cd AI-Engineering-Practice-Projects
```

### 2. Install dependencies
```bash
pip install openai python-dotenv requests beautifulsoup4 gradio pydantic
```

### 3. Configure environment variables
Copy `.env.example` to `.env` and add your Groq API key:
```bash
copy .env.example .env
```
Inside `.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the scripts

- **Run first LLM call:**
  ```powershell
  python first_call.py
  ```

- **Run interactive CLI chat:**
  ```powershell
  python interactive_chat.py
  ```

- **Launch the AI Website Summarizer (Web UI):**
  ```powershell
  python summarizer.py
  ```

- **Run structured JSON output with Pydantic:**
  ```powershell
  python structured_output.py
  ```

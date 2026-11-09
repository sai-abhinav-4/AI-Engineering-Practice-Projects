# AI Engineering Practice Projects

This repository contains hands-on practice projects and exercises from the AI BootCamp.

## First Class: LLM API Fundamentals

- **`first_call.py`**: Basic setup to connect to an LLM provider (Groq) using OpenAI-compatible SDK and execute a chat completion.
- **`interactive_chat.py`**: Real-time streaming CLI chat application demonstrating conversation memory and token streaming (`stream=True`).

## Setup & Running

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sai-abhinav-4/AI-Engineering-Practice-Projects.git
   cd AI-Engineering-Practice-Projects
   ```

2. **Install dependencies:**
   ```bash
   pip install openai python-dotenv
   ```

3. **Configure environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env
     ```
   - Add your `GROQ_API_KEY` in `.env`.

4. **Run the scripts:**
   ```bash
   python first_call.py
   python interactive_chat.py
   ```

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load GROQ_API_KEY from .env
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

# Using the fastest & cheapest general-purpose model
MODEL = "openai/gpt-oss-20b"

# Initialize conversation history with a system prompt
messages = [
    {
        "role": "system",
        "content": "You are a helpful and witty AI assistant. Keep responses engaging and concise.",
    }
]

print("=" * 50)
print(f"Chat initialized with model: {MODEL}")
print("Type 'quit' or 'exit' to end the session.")
print("=" * 50)

while True:
    user_input = input("\nYou: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ["quit", "exit"]:
        print("Goodbye!")
        break

    # Append user question to history
    messages.append({"role": "user", "content": user_input})

    # Stream the response in real time
    print("\nAssistant: ", end="", flush=True)
    response_stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        stream=True,
    )

    full_reply = ""
    for chunk in response_stream:
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
        full_reply += content
    print()

    # Append assistant's response to maintain conversation memory
    messages.append({"role": "assistant", "content": full_reply})

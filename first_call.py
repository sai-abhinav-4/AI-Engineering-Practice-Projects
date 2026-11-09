import os
# pip install python-dotenv
from dotenv import load_dotenv
# pip install openai
from openai import OpenAI

load_dotenv()                 # loads everything from .env

client = OpenAI(
    api_key = os.getenv("GROQ_API_KEY"),
    base_url = "https://api.groq.com/openai/v1",
)

response = client.chat.completions.create(
    model = "allam-2-7b",
    messages = [
        {"role": "system", "content":"You are a witty travel guide"},
        {"role": "user", "content":"suggest one thing to do in Hyderabad."},
    ],
)
print(response.choices[0].message.content)

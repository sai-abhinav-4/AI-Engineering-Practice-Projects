# memory_demo.py
# Block 10 — Version 1: memory with the history typed by hand
# (shows the IDEA: the model only "remembers" because WE re-send past messages).
# Run:  python memory_demo.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

load_dotenv()
# Groq wrapper using LangChain's ChatOpenAI
model = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    temperature=0.3,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly tutor."),
    MessagesPlaceholder("history"),     # past turns slot in here
    ("human", "{question}"),
])
chain = prompt | model

# we hardcode the history here just to demonstrate
history = [HumanMessage("My name is Aarav."), AIMessage("Hi Aarav!")]

answer = chain.invoke({"history": history, "question": "What's my name?"})
print(answer.content)   # -> "Your name is Aarav."  (it "remembered" because we re-sent history)

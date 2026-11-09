import os
import sys
from dotenv import load_dotenv

# Add parent directory to sys.path so scraper can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scraper import fetch_website_contents   

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template(            
    "Give a short, friendly summary of this website:\n\n{website}"
)

# Groq wrapper using LangChain's ChatOpenAI
model = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    temperature=0.3,
)

parser = StrOutputParser()                          
chain = prompt | model | parser                       

def summarize(url):
    return chain.invoke({"website": fetch_website_contents(url)})   

if __name__ == "__main__":
    print(summarize("https://anthropic.com"))

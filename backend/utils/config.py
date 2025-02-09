import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def create_llm():
    return ChatGroq(model="llama3-8b-8192")

def create_deepseek_llm():
    return ChatGroq(model="deepseek-3b-8k")
from utils.models import ParallelState
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from agents.base import llm

def SQLi_agent(state: ParallelState):
  pass
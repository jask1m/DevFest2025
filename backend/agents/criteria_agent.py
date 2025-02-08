from agents.base import llm
from utils.models import Criteria, GraphState
from langgraph.types import Command
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain.output_parsers import OutputFixingParser
from langchain.prompts import ChatPromptTemplate
from typing import List
import json

class OutputSchema(BaseModel):
  name: str = Field(description="title of the selected critera")

def format_criteria(criteria_list: List[Criteria]) -> str:
    """Format a list of criteria objects for the prompt."""
    return "\n".join([
        f"""Title: {criteria.title}
Description: {json.dumps(criteria.criteria, indent=2)}
---""" 
        for criteria in criteria_list
    ])

def prevent_hallucination(res_title: str, state: GraphState) -> str:
    if res_title == "NO_MATCHES":
        return res_title
    existing_titles = {criteria.title for criteria in state.existing_criteria}
    return res_title if res_title in existing_titles else "NO_MATCHES"

TEMPLATE = """You are a network security expert tasked with analyzing network usage descriptions and matching them to existing monitoring criteria.

EXISTING CRITERIA:
{criteria_list}

USER DESCRIPTION:
{description}

Your task is to:
1. Analyze the user's description of their network usage needs
2. Compare it against the existing criteria profiles
3. Return EXACTLY "NO_MATCHES" if any of these conditions are true:
   - The existing criteria list is empty, blank, or null
   - No criteria matches the user description with high confidence
   - The user description is too vague or ambiguous to make a definitive match
   - You're unsure about the match quality
4. Otherwise, return the EXACT title of the single best matching criteria

CRITICAL REQUIREMENTS:
- You MUST return "NO_MATCHES" if there is ANY doubt about the match quality
- You MUST return "NO_MATCHES" if the criteria list is empty or blank
- If returning a match, the title MUST be copied exactly from the existing criteria list
- Do NOT return modified, partial, or similar-looking titles
- Do NOT attempt to combine or modify existing criteria titles
- Only return a SINGLE exact match, never multiple matches
"""

prompt = ChatPromptTemplate.from_template(template=TEMPLATE)
parser = PydanticOutputParser(pydantic_object=OutputSchema)
output_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

def criteria_agent(state: GraphState) -> Command:
  criteria_list = format_criteria(state.existing_criteria)
  chain = prompt | llm | output_parser

  try:
    res = chain.invoke({
      "criteria_list": criteria_list,
      "description": state.description
    })
    print("initial res fetched: ", res)
    res_title = res.name
    res_title = prevent_hallucination(res_title, state)

    if res_title != "NO_MATCHES":
        matching_criteria = next((c for c in state.existing_criteria if c.title == res_title), None)
        if matching_criteria:
            print("Selected criteria title: ", res_title)
            print("sending to qa agent ....")
            return Command(update={"selected_criteria": res_title}, goto="qa_agent")
        else:
            raise ValueError("Returned title does not match any existing criteria!")
    else:        
        print("No good matches found.")
        print("sending to new_criteria_agent ....")
        return Command(goto="new_criteria_agent")
  except Exception as e:
    print("error invoking the chain:", e)
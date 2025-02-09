from agents.base import llm
from utils.models import Criteria, GraphState
from langgraph.types import Command
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import ChatPromptTemplate
from typing import List
import json

response_schema = ResponseSchema(
    name="title",
    description="The title of the matching criteria or 'NO_MATCHES' if no good match is found",
)


def format_criteria(criteria_list: List[Criteria]) -> str:
    """Format a list of criteria objects for the prompt, including scapy_str in Berkeley Packet Format."""
    return "\n".join(
        [
            f"""Title: {criteria.title}
Description: {json.dumps(criteria.criteria, indent=2)}
Scapy String: {criteria.scapy_str}
---"""
            for criteria in criteria_list
        ]
    )


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

{format_instructions}"""

prompt = ChatPromptTemplate.from_template(template=TEMPLATE)
output_parser = StructuredOutputParser.from_response_schemas([response_schema])


def criteria_agent(state: GraphState) -> Command:
    print("Reached the Criteria Agent node!")
    criteria_list = format_criteria(state.existing_criteria)
    format_instructions = output_parser.get_format_instructions()
    chain = prompt | llm | output_parser

    try:
        res = chain.invoke(
            {
                "criteria_list": criteria_list,
                "description": state.description,
                "format_instructions": format_instructions,
            }
        )
        print("initial res fetched: ", res)
        res_title = res["title"]
        res_title = prevent_hallucination(res_title, state)

        if res_title != "NO_MATCHES":
            matching_criteria = next(
                (c for c in state.existing_criteria if c.title == res_title), None
            )
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
        print("ERROR invoking the chain in criteria_agent:", e)

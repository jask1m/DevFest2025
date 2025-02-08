from utils.models import GraphState
from langgraph.types import Command
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import ChatPromptTemplate
from agents.base import llm
from utils.models import Criteria
import json

qa_schema = [
    ResponseSchema(
        name="decision",
        description="Either 'VALID' if the criteria matches the use case well, or 'INVALID' if it needs improvement"
    ),
    ResponseSchema(
        name="feedback",
        description="Detailed analysis of the criteria's strengths and areas for improvement"
    )
]

def format_criteria(criteria: Criteria) -> str:
    if isinstance(criteria, list):
        criteria = criteria[0]
    
    return f"""Title: {criteria.title}
Description: {criteria.description}
Criteria Details:
{json.dumps(criteria.criteria, indent=2)}"""

TEMPLATE = """You are a network security quality assurance AI Agent tasked with assessing the quality of a network criteria that is to be monitored based on a user's description of their network usage needs.
USER DESCRIPTION:
{description}
SELECTED CRITERIA:
{the_criteria}

Your task is to analyze the alignment between the user's needs and the selected criteria. Follow these steps:

1. Comprehension Analysis:
   - Does the criteria demonstrate a clear understanding of the user's network usage scenario?
   - Are all key aspects of the user's description addressed in the criteria?

2. Technical Assessment:
   - Are the selected protocols appropriate for this use case?
   - Do the specified ports match the described network services?
   - Are the track_fields sufficient to monitor the described activities?
   - Are the alert conditions relevant and properly thresholded?

3. Security Coverage:
   - Does the criteria adequately address potential security concerns for this use case?
   - Are there any monitoring gaps that could leave vulnerabilities?

4. Practical Implementation:
   - Is the criteria specific enough to be implemented?
   - Are there any redundant or unnecessary elements?

Based on your analysis, provide:
1. A decision of 'VALID' or 'INVALID'
2. Detailed feedback including:
   - Specific strengths of the current criteria
   - Areas that need improvement (if any)
   - Concrete suggestions for enhancement
   
Your feedback will be used to either approve the criteria or guide improvements, so be thorough and specific.

{format_instructions}"""

prompt = ChatPromptTemplate.from_template(template=TEMPLATE)
qa_parser = StructuredOutputParser.from_response_schemas(qa_schema)

def qa_agent(state: GraphState) -> Command:
  print("Reached the QA Agent node!")
  print("updated 'selected_criteria' value: ", state.selected_criteria)

  if state.sent_from and state.sent_from == "new_criteria_agent":
    return Command(
      update={
        "approved": True}, 
      )

  selected_criteria = next(
      (c for c in state.existing_criteria if c.title == state.selected_criteria),
      None
    )
  if selected_criteria is None:
        raise ValueError("No matching criteria found")
  print("selected_criteria: ", selected_criteria)

  chain = prompt | llm | qa_parser
  try:
    res = chain.invoke({
      "description": state.description,
      "the_criteria": format_criteria(selected_criteria),
      "format_instructions": qa_parser.get_format_instructions()
    })
    decision = res["decision"]
    feedback = res["feedback"]
    print("qa_agent response: ", res)

    if decision == "VALID":
     return Command(
        update={"approved": True},
      )
    else:
     return Command(
        update={"feedback": feedback, "sent_from": "qa_agent"},
        goto="new_criteria_agent"
     )

  except Exception as e:
    print("error invoking the chain in qa_agent:", e)



from utils.models import GraphState
from langgraph.types import Command
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import ChatPromptTemplate
from agents.base import llm

new_criteria_schema = [
    ResponseSchema(
        name="title",
        description="A short, snake_case title that describes the network monitoring use case"
    ),
    ResponseSchema(
        name="description", 
        description="A clear description of the use case and what type of network traffic should be monitored"
    ),
    ResponseSchema(
        name="criteria",
        description="A JSON object containing the monitoring criteria including protocols, ports, track_fields, and alert_conditions"
    )
]

TEMPLATE = """You are a network security expert tasked with creating monitoring criteria for specific network usage patterns.

Here is an example of a well-structured monitoring criteria:

{{"title": "backend_infrastructure",
"description": "This use case is for when the network is used to manage backend servers and databases. This use case is appropriate for ensuring that database and backend API server requests are validated and not coming from unauthorized or foreign locations.",
"criteria": {{
    "protocols": ["TCP"],
    "ports": [3306, 5432, 6379, 27017, 8080, 443],
    "ip_ranges": ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"],
    "track_fields": [
        "source_ip",
        "destination_ip",
        "transport_layer.protocol",
        "transport_layer.source_port",
        "transport_layer.destination_port",
        "transport_layer.flags",
        "payload.length"
    ],
    "alert_conditions": {{
        "unauthorized_ip": "source_ip not in ip_ranges",
        "suspicious_ports": "destination_port not in ports",
        "large_payload": "payload.length > 1000000"
    }}
}}}}

Based on the user's description below, create a new monitoring criteria following the same structure.

USER DESCRIPTION:
{description}

REQUIREMENTS:
1. Return a valid JSON object with exactly these fields: title (snake_case), description (string), and criteria (object)
2. The criteria object must include: protocols (array), ports (array), track_fields (array), and alert_conditions (object)
3. Remove any comments or annotations from the JSON - it must be pure, valid JSON
4. Ensure all special characters are properly escaped

{qa_feedback}

{format_instructions}"""

prompt = ChatPromptTemplate.from_template(template=TEMPLATE)
criteria_parser = StructuredOutputParser.from_response_schemas(new_criteria_schema)

def new_criteria_agent(state: GraphState) -> Command:
  print("Reached the New Criteria Agent node!")
  qa_feedback = ""
  if state.sent_from and state.sent_from == "qa_agent" and state.feedback:
    qa_feedback = f"""
      QUALITY ASSURANCE FEEDBACK:
      The previous criteria had the following issues that need to be addressed:
      {state.feedback}

      Please ensure the new criteria addresses these concerns.
    """

  chain = prompt | llm | output_parser
  try:
    res = chain.invoke({
      "description": state.description,
      "qa_feedback": qa_feedback
    })
    print("new criteria agent response: ", res)
    criteria_dict = res["criteria"]

    new_criteria = Criteria(
            title=res["title"],
            description=res["description"],
            criteria=criteria_dict
        )
    updated_criteria = state.existing_criteria + [new_criteria]
    return Command(
            update={
                "existing_criteria": updated_criteria,
                "selected_criteria": new_criteria.title,
                "sent_from": "new_criteria_agent",
                "feedback": None
            },
            goto="qa_agent"
        )
  except Exception as e:
    print("error invoking the chain in new_criteria_agent:", e)
    return Command(goto="new_criteria_agent")
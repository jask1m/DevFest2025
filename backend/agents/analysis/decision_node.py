from utils.models import ParallelState
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from agents.base import reasoning_llm

output_schema = [
    ResponseSchema(
        name="threat_detected",
        description="A boolean value: true if any security threat is detected, false if the packet appears safe"
    ),
    ResponseSchema(
        name="details",
        description="Comprehensive analysis summarizing all detected threats and their severity levels from the parallel agent analysis, or confirmation of packet safety if no threats detected"
    )
]

#TODO add the general packet analysis in the proompt
TEMPLATE = """You are a security decision agent. Below are the analyses from 3 specialized packet analysis agents. Each agent provides explicit feedback in if it determined a specific malicious request. Analyze the following output responses to make a final decision on whether a threat is present in the packet.

XSS AGENT ANALYSIS FINDINGS:
{xss_agent_msg}
SQL INJECTION AGENT ANALYSIS FINDINGS:
{SQLi_agent_msg}

Your task is to analyze these findings and provide a structured response following the exact format below:

{format_instructions}

Example outputs:

If threat detected:
{{
    "threat_detected": true,
    "details": "Critical security threat identified. XSS attack detected in packet payload attempting cookie theft and data exfiltration. Supporting evidence from XSS agent shows malicious script injection pattern '<script>document.cookie.send()...</script>'. This poses significant risk of session hijacking and unauthorized data access. Immediate packet blocking and source IP investigation recommended."
}}

If no threat detected:
{{
    "threat_detected": false,
    "details": "All security agents report no malicious patterns. XSS agent confirms absence of script injection attempts. SQL injection agent verifies no database manipulation attempts. Packet appears to contain legitimate traffic."
}}

Remember:
- Be conservative in threat detection - only flag clear security threats with strong supporting evidence
- If one agent determines that a threat exists, that is enough for you to flag it as such
- Provide comprehensive details supporting your decision
- Include specific evidence from agent findings when explaining threats
- Make clear, decisive determinations based on the available information"""

prompt = ChatPromptTemplate.from_template(template=TEMPLATE)
parser = StructuredOutputParser.from_response_schemas(output_schema)

def decision_node(state: ParallelState):
  if not all([state.xss_agent_msg, state.SQLi_agent_msg, state.payload_agent_msg]):
    print("WARNING: not all agents provided feedback!")
    
    #TODO: proof of concept for now
    if not state.payload_agent_msg:
      print("IT's okay though....")
    if not state.xss_agent_msg or not state.SQLi_agent_msg:
      print("wait actualy umm ....")
    # raise ValueError("All agents must provide feedback")
  
  chain = prompt | reasoning_llm | parser
  try:
    res = chain.invoke({
      "xss_agent_msg": state.xss_agent_msg,
      "SQLi_agent_msg": state.SQLi_agent_msg,
      # "payload_agent_msg": state.payload_agent_msg,
      "format_instructions": parser.get_format_instructions()
    })
    print("decision node response: ", res)
    state.feedback = res["details"]
    state.threat_detected = res["threat_detected"]

    return {
      "threat_detected": state.threat_detected,
      "feedback": state.feedback
    }

  except Exception as e:
    print("ERROR invoking the chain in decision_node:", e)
  
  return {"next": "END"}
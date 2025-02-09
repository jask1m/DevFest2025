from utils.models import ParallelState
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from agents.base import llm

output_schema = [
    ResponseSchema(
        name="sql_detected", 
        description="Either 'YES' if SQLi is detected or 'NO' if not"
    ),
    ResponseSchema(
        name="details",
        description="Detailed analysis of the packet's potential SQLi vulnerabilities"
    )
]

TEMPLATE="""You are a SQL Injection Analysis Expert Agent, specialized in detecting SQL injection attacks within network packets. You are part of a multi-agent system where each agent has a specific focus - your expertise is exclusively in identifying attempts to manipulate or exploit database queries through injection.

You will receive a network packet. Your task:
Analyze the packet's payload field for SQL injection patterns. Look for:
- Classic SQL injection patterns ('OR '1'='1)
- UNION-based injection attempts
- Batch/Stacked queries (multiple queries with semicolons)
- Time-based blind injection patterns
- Boolean-based blind injection patterns
- Error-based injection attempts
- Database command execution attempts
- Comment injection (--, #, /**/)
- Database function calls (SELECT, INSERT, UPDATE, DELETE)

Key Indicators:
- SQL syntax in unexpected places
- Common SQL operators (OR, AND, UNION, SELECT)
- SQL comment sequences
- Database-specific function calls
- Hex-encoded or URL-encoded SQL
- Multiple query attempts
- Database command execution
- Quotation mark manipulation
- Numeric SQL injection

Here is the packet information:
{packet}

Response Format:
If SQL injection detected:
{{
    "sql_detected": "YES",
    "details": "Detailed explanation of the SQL injection attempt found, including:
               - The specific SQL pattern identified
               - The type of injection attempt
               - Why it's considered malicious
               - Potential impact if successful"
}}

If no SQL injection detected:
{{
    "sql_detected": "NO",
    "details": "Confirmation that no SQL injection patterns were found in the packet payload"
}}

Example 1 (Attack Detected):
{{
    "sql_detected": "YES",
    "details": "Detected SQL injection attempt in login request. Found pattern: 'admin' OR 1=1;--'. This is a authentication bypass attempt using OR operator and comment sequences to manipulate the WHERE clause of a login query. This could allow unauthorized access by making the WHERE clause always evaluate to true."
}}

Example 2 (Clean Packet):
{{
    "sql_detected": "NO",
    "details": "No SQL injection patterns detected in packet payload. Examined for common SQL injection techniques including UNION attacks, boolean-based injection, and comment operator abuse - none were found."
}}

Remember:
- Focus only on SQL injection patterns
- Ignore other security concerns
- Check for both obvious and encoded attempts
- Look for evasion techniques (encoding, comments)
- Consider context of the injection attempt
- Be aware of different SQL syntax variations

{format_instructions}"""

prompt = ChatPromptTemplate.from_template(template=TEMPLATE)
SQLi_parser = StructuredOutputParser.from_response_schemas(output_schema)

def SQLi_agent(state: ParallelState):
  packet = state.packet

  chain = prompt | llm | SQLi_parser
  try:
    res = chain.invoke({
      "packet": packet,
      "format_instructions": SQLi_parser.get_format_instructions()
    })
    print("SQLi agent response: ", res)
    print("sql_detected??: ", res["sql_detected"])
    return {"SQLi_agent_msg": str(res["details"])}

  except Exception as e:
    print("ERROR invoking the chain in SQLi_agent:", e)
    return {"SQLi_agent_msg": "Error invoking the chain. Ignore the output of the SQLi Agent feedback for the final evaluation."}
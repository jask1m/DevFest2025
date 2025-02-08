from utils.models import ParallelState

def root_node(state: ParallelState):
  if not state.criteria or not state.packet:
    raise ValueError("Packet and criteria must be provided")
  
  state.payload_msg = ""
  state.xss_agent_msg = ""
  state.SQLi_agent_msg = ""
  state.payload_agent_msg = ""
  state.threat_detected = False
  state.feedback = ""
  return {
        "next": [
            "xss_agent",
            "SQLi_agent",
            "payload_agent",
        ]
    }
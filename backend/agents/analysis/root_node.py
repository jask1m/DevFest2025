from utils.models import ParallelState

def root_node(state: ParallelState):
  if not state.packet:
    raise ValueError("Packet and criteria must be provided")
  return {
        "next": [
            "xss_agent",
            "SQLi_agent",
            # "payload_agent",
        ]
    }
from pydantic import BaseModel
from typing import Any, List, Optional, Dict

class Criteria(BaseModel):
  title: str
  description: str
  criteria: dict[str, Any]

class GraphState(BaseModel):
  description: str
  existing_criteria: List[Criteria] 
  selected_criteria: Optional[str] = None
  sent_from: Optional[str] = None
  feedback: Optional[str] = None
  approved: bool = False

class ParallelState(BaseModel):
  packet: Dict[str, Any] # todo set to erik's schema
  xss_agent_msg: str
  SQLi_agent_msg: str
  payload_agent_msg: str
  threat_detected: bool
  feedback: str

from pydantic import BaseModel
from typing import Any, List, Optional

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
  criteria: Dict[str, Any] # todo: should this be Criteria obj?
  packet: Dict[str, Any] # todo set to erik's schema
  payload_msg: str
  dns_msg: str
  port_msg: str
  protocol_msg: str
  threat_detected: bool
  feedback: str

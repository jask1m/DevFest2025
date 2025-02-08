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
  criteria: Dict[str, Any]
  packet: Dict[str, Any] # todo fix schema

  # msg for each agent node
  payload_msg: str

  threat_detected: bool
  feedback: str

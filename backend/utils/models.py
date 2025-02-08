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


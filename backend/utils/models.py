from pydantic import BaseModel
from typing import Any

class Criteria(BaseModel):
  title: str
  description: str
  criteria: dict[str, Any]

class GraphState(BaseModel):
  pass


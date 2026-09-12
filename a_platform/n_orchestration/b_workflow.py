from typing import List, Dict, Any
from pydantic import BaseModel, Field

class WorkflowStep(BaseModel):
    name: str
    dependencies: List[str] = Field(default_factory=list)

class Workflow(BaseModel):
    id: str
    steps: List[WorkflowStep] = Field(default_factory=list)

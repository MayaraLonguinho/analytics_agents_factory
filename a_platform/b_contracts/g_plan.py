
from pydantic import BaseModel, Field
from typing import List, Any
from .b_task import ProjectTask

class ProjectPlan(BaseModel):
    project_id: str
    domain: str = ""
    tasks: List[ProjectTask] = Field(default_factory=list)
    run_commands: List[str] = Field(default_factory=list)

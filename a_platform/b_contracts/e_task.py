from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from .g_artifact import Artifact

class ProjectTask(BaseModel):
    model_config = {"extra": "forbid"}
    task_id: str
    name: str
    description: str = ""
    assigned_agent: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    required_mcps: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    expected_artifacts: List[str] = Field(default_factory=list)
    commands: List[str] = Field(default_factory=list)
    validators: List[str] = Field(default_factory=list)
    status: str = "PENDING"

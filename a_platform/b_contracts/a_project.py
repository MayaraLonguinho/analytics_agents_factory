from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from a_platform.b_contracts.b_task import ProjectTask
from a_platform.b_contracts.c_artifact import Artifact

class ProjectContext(BaseModel):
    model_config = {"extra": "forbid"}
    project_id: str
    project_name: str
    project_path: str
    domain: str = ""
    requested_capabilities: List[str] = Field(default_factory=list)
    architecture: Dict[str, Any] = Field(default_factory=dict)
    plan: List[ProjectTask] = Field(default_factory=list)
    generated_artifacts: List[Artifact] = Field(default_factory=list)
    runtime_information: Dict[str, Any] = Field(default_factory=dict)

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class Artifact(BaseModel):
    name: str
    path: str
    content: Optional[str] = None

class ProjectRequest(BaseModel):
    project_id: str
    prompt: str
    dataset_path: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class DiscoveryResult(BaseModel):
    project_id: str
    business_context: str = ""
    domain: str = ""
    dataset_profile: Dict[str, Any] = Field(default_factory=dict)
    assumptions: List[str] = Field(default_factory=list)

class ArchitectureDecision(BaseModel):
    project_id: str
    decision: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ProjectTask(BaseModel):
    task_id: str
    name: str
    description: str = ""
    assigned_agent: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    status: str = "PENDING"
    dependencies: List[str] = Field(default_factory=list)

class ProjectPlan(BaseModel):
    project_id: str
    tasks: List[ProjectTask] = Field(default_factory=list)
    status: str = "PENDING"

Task = ProjectTask

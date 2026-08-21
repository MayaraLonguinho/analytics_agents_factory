from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ProjectPlan(BaseModel):
    """Canonical plan contract for execution sequencing."""
    project_id: str
    name: str
    domain: str
    phases: List[str] = Field(default_factory=list)
    tasks: List[str] = Field(default_factory=list)
    milestones: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    generated_by: Optional[str] = None

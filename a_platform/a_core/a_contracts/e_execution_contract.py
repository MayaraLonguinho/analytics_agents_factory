from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class Artifact(BaseModel):
    artifact_id: str
    name: str
    content: Any
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ExecutionResult(BaseModel):
    task_id: str
    success: bool = False
    output: str = ""
    error: Optional[str] = None
    artifacts: List[Artifact] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

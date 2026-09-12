from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class ExecutionResult(BaseModel):
    """Result of an execution task."""
    task_id: str
    success: bool
    output: str = ""
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

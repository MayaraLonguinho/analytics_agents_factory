from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ExecutionResult(BaseModel):
    model_config = {"extra": "forbid"}
    execution_id: str = ""
    task_id: str = ""
    command: List[str] = Field(default_factory=list)
    working_directory: str = ""
    status: str = "NOT_EXECUTED"
    return_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    started_at: float = 0.0
    finished_at: float = 0.0
    duration: float = 0.0
    timeout: float = 0.0
    policy_decision: str = ""
    error: str = ""
    evidence: str = ""

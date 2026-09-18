from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CommandExecutionResult(BaseModel):
    """Typed evidence record for a single command execution."""
    model_config = {"extra": "forbid"}
    task_id: str = ""
    command: List[str] = Field(default_factory=list)   # argv — no shell string
    executable: str = ""                                # args[0]
    working_directory: str = ""
    status: str = "NOT_EXECUTED"                        # ALLOWED | DENIED | SUCCESS | FAILED | TIMEOUT
    return_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    started_at: float = 0.0
    finished_at: float = 0.0
    duration: float = 0.0
    timeout: float = 120.0
    policy_decision: str = ""                           # "ALLOWED" | "DENIED: <reason>"
    error: str = ""


class ExecutionResult(BaseModel):
    model_config = {"extra": "forbid"}
    execution_id: str = ""
    task_id: str = ""                                   # last failed task (backward compat)
    command: List[str] = Field(default_factory=list)    # last failed command (backward compat)
    working_directory: str = ""
    status: str = "NOT_EXECUTED"                        # PASSED | FAILED | NOT_EXECUTED
    return_code: Optional[int] = None
    stdout: str = ""                                    # aggregated stdout
    stderr: str = ""                                    # aggregated stderr
    started_at: float = 0.0
    finished_at: float = 0.0
    duration: float = 0.0
    timeout: float = 0.0
    policy_decision: str = ""
    error: str = ""
    evidence: str = ""
    commands: List[CommandExecutionResult] = Field(default_factory=list)

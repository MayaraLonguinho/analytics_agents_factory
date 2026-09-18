from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ValidationResult(BaseModel):
    model_config = {"extra": "forbid"}
    status: str = "NOT_EXECUTED"
    evidence: str = ""
    details: str = ""
    errors: List[str] = Field(default_factory=list)
    origin: str = ""

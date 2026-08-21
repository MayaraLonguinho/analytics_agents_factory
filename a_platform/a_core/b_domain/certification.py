from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class CertificationResult(BaseModel):
    """Result of the certification and quality assurance phase."""
    project_id: str
    passed: bool
    issues: List[str] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    feedback: Optional[str] = None

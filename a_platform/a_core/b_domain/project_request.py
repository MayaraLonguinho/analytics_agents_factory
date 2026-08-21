from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ProjectRequest(BaseModel):
    """Canonical request contract for ingesting project intent."""
    request: str
    domain: Optional[str] = None
    source: str = "cli"
    dataset_source: Optional[str] = None
    dataset_profile: Dict[str, Any] = Field(default_factory=dict)
    answers: Dict[str, str] = Field(default_factory=dict)
    architecture_constraints: List[str] = Field(default_factory=list)
    technology_preferences: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    preferred_stack: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_raw(cls, raw_request: str, **kwargs) -> "ProjectRequest":
        normalized = (raw_request or "").strip()
        if not normalized:
            raise ValueError("request cannot be empty")
        return cls(request=normalized, **kwargs)

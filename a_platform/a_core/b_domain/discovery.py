from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class DiscoveryResult(BaseModel):
    """Structured result of input discovery and normalization."""
    project_objective: str = ""
    domain: Optional[str] = None
    request: str = ""
    source: str = "cli"
    dataset_source: Optional[str] = None
    dataset_profile: Dict[str, Any] = Field(default_factory=dict)
    requirements: Dict[str, Any] = Field(default_factory=dict)
    architecture_constraints: List[str] = Field(default_factory=list)
    technology_preferences: List[str] = Field(default_factory=list)
    decisions: Dict[str, str] = Field(default_factory=dict)
    assumptions: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    unresolved_items: List[str] = Field(default_factory=list)
    backend_requirement: str = ""
    frontend_requirement: str = ""
    database_requirement: str = ""
    infrastructure_requirement: str = ""
    testing_requirement: str = ""
    documentation_requirement: str = ""
    discovered_metadata: Dict[str, Any] = Field(default_factory=dict)
    questions: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    preferred_stack: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

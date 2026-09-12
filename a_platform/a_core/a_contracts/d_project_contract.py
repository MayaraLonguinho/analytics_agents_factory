from datetime import datetime, timezone
from typing import Any, Dict, List
from pydantic import BaseModel, Field

class Project(BaseModel):
    """Canonical project definition resulting from planning and generation."""
    project_id: str
    name: str
    domain: str
    status: str = "REQUESTED"
    request: str = ""
    description: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
    artifacts: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

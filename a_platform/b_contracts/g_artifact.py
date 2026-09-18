from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class Artifact(BaseModel):
    model_config = {"extra": "forbid"}
    identity: str
    name: str
    path: str
    type: str
    content: Any = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    producer: Optional[str] = None

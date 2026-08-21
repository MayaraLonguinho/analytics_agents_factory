from datetime import datetime, timezone
from pydantic import BaseModel, Field

class Artifact(BaseModel):
    """Represents a generated code artifact."""
    name: str
    path: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

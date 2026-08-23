from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class ProjectResponseDTO:
    success: bool
    project_id: str
    status: str
    message: Optional[str] = None
    error: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)

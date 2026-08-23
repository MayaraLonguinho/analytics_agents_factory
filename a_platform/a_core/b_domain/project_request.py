from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class ProjectRequest:
    prompt: str
    dataset_path: Optional[str] = None
    domain: Optional[str] = None
    project_id: str = field(default_factory=lambda: "proj_default")
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Phase 3
    discovery_data: Dict[str, Any] = field(default_factory=dict)
    dataset_profile: Dict[str, Any] = field(default_factory=dict)
    
    # Phase 4
    architecture_decision: Dict[str, Any] = field(default_factory=dict)
    graph_representation: Dict[str, Any] = field(default_factory=dict)

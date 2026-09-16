from dataclasses import dataclass, field
from typing import List, Dict, Any
from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.c_artifact import Artifact

@dataclass
class GenerationContext:
    project_context: ProjectContext
    capabilities_requested: List[str] = field(default_factory=list)
    resolved_capabilities: List[str] = field(default_factory=list)
    artifacts: List[Artifact] = field(default_factory=list)

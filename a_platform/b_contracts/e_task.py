from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from .g_artifact import Artifact

class ProjectTask(BaseModel):
    model_config = {"extra": "forbid"}
    task_id: str
    name: str
    description: str = ""
    assigned_agent: Optional[str] = None
    capability: Optional[str] = None
    capabilities: List[str] = Field(default_factory=list)
    preferred_skill: Optional[str] = None
    preferred_skills: List[str] = Field(default_factory=list)
    required_skills: List[str] = Field(default_factory=list)
    required_mcps: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    expected_artifacts: List[str] = Field(default_factory=list)
    commands: List[str] = Field(default_factory=list)
    validators: List[str] = Field(default_factory=list)
    status: str = "PENDING"

    def get_all_capabilities(self) -> List[str]:
        """Retorna lista consolidada e deduplicada de capabilities mantendo a ordem."""
        caps = list(self.capabilities)
        if self.capability and self.capability not in caps:
            caps.append(self.capability)
        return caps

    def get_all_preferred_skills(self) -> List[str]:
        """Retorna lista consolidada e deduplicada de preferred_skills mantendo a ordem."""
        prefs = list(self.preferred_skills)
        if self.preferred_skill and self.preferred_skill not in prefs:
            prefs.append(self.preferred_skill)
        return prefs

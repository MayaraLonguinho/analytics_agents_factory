from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class AgentCapability(BaseModel):
    name: str
    description: str

class AgentContract(BaseModel):
    model_config = {"extra": "forbid"}
    agent_id: str
    name: str
    description: str
    responsibility: str
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
    allowed_skills: List[str] = Field(default_factory=list)
    allowed_mcps: List[str] = Field(default_factory=list)
    applicable_rules: List[str] = Field(default_factory=list)
    required_context: List[str] = Field(default_factory=list)
    capabilities: List[AgentCapability] = Field(default_factory=list)
    version: str = "1.0.0"
    tags: List[str] = Field(default_factory=list)

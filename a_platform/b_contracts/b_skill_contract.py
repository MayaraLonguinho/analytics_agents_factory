from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class SkillExecutionType(str, Enum):
    NATIVE = "native"
    LLM = "llm"

class ParameterDefinition(BaseModel):
    name: str
    data_type: str
    required: bool = True
    constraints: Dict[str, Any] = Field(default_factory=dict)

class SkillContract(BaseModel):
    model_config = {"extra": "forbid"}
    skill_id: str = "default_skill"
    name: str = "Default Skill"
    description: str = "Default description"
    execution_type: SkillExecutionType = SkillExecutionType.NATIVE
    version: str = "1.0.0"
    input_schema: List[ParameterDefinition] = Field(default_factory=list)
    output_schema: List[ParameterDefinition] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    compatible_agents: List[str] = Field(default_factory=list)
    required_mcps: List[str] = Field(default_factory=list)
    required_brain_context: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    source: str = ""
    category: str = ""
    author: str = ""
    documentation_url: str = ""

BaseSkill = SkillContract
CORE_SKILL_CONTRACTS = {}

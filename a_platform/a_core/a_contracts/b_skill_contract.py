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
    """Contract defining a skill's interface and execution model."""
    skill_id: str
    name: str
    description: str
    execution_type: SkillExecutionType
    version: str = "1.0.0"
    input_schema: List[ParameterDefinition] = Field(default_factory=list)
    output_schema: List[ParameterDefinition] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)  # Skill IDs
    compatible_agents: List[str] = Field(default_factory=list)  # Agent IDs
    required_mcps: List[str] = Field(default_factory=list)
    required_brain_context: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    source: str = ""  # Where the skill is implemented
    category: str = ""  # discovery, dataset, analytics, data_engineering, development, quality
    author: str = ""
    documentation_url: str = ""

CORE_SKILL_CONTRACTS = {}

BaseSkill = SkillContract

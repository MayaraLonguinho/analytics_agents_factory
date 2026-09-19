"""
Skill Contract interface and definitions.
Re-exports canonical definitions from a_platform.b_contracts.c_skill_contract.
"""
from a_platform.b_contracts.c_skill_contract import (
    SkillContract,
    BaseSkill,
    ParameterDefinition,
    SkillExecutionType,
    CORE_SKILL_CONTRACTS,
)

__all__ = [
    "SkillContract",
    "BaseSkill",
    "ParameterDefinition",
    "SkillExecutionType",
    "CORE_SKILL_CONTRACTS",
]

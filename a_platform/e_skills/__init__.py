"""Central Skills Architecture - Analytics Agents Factory.

Skills are reusable, composable units of work.
Skills encapsulate execution logic (native, LLM, or MCP-based).
Agents coordinate Skills through the Skill Registry and Skill Router.
"""
from a_platform.e_skills.skill_contract import SkillContract, BaseSkill, ParameterDefinition, SkillExecutionType
from a_platform.e_skills.skill_registry import SkillRegistry
from a_platform.e_skills.skill_index import SkillIndex
from a_platform.e_skills.skill_router import SkillRouter, SkillSelection, SkillSelectionItem, SkillRoutingError

__all__ = [
    "SkillContract",
    "BaseSkill",
    "ParameterDefinition",
    "SkillExecutionType",
    "SkillRegistry",
    "SkillIndex",
    "SkillRouter",
    "SkillSelection",
    "SkillSelectionItem",
    "SkillRoutingError",
]

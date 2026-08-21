"""Skill Registry - Central registry for all skills.

Manages skill discovery, validation, and execution coordination.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .skill_contract import SkillContract, SkillExecutionType, ParameterDefinition


class SkillRegistry:
    """Registry for managing and accessing skills."""

    def __init__(self, skills_root: Optional[Path] = None):
        if skills_root is None:
            self.skills_root = Path(__file__).resolve().parents[1] / "d_skills"
        else:
            self.skills_root = Path(skills_root).resolve()

        self.skills: Dict[str, SkillContract] = {}
        self.skills_by_category: Dict[str, List[SkillContract]] = {}
        self.skills_by_agent: Dict[str, List[SkillContract]] = {}
        self._load_skills()

    def _load_skills(self) -> None:
        """Load skill declarations from YAML."""
        declarations_file = self.skills_root / "declarations" / "skills.yaml"
        if not declarations_file.exists():
            return

        with declarations_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        for skill_data in data.get("skills", []):
            skill = self._parse_skill(skill_data)
            self.skills[skill.skill_id] = skill

            # Index by category
            if skill.category:
                if skill.category not in self.skills_by_category:
                    self.skills_by_category[skill.category] = []
                self.skills_by_category[skill.category].append(skill)

            # Index by compatible agents
            for agent_id in skill.compatible_agents:
                if agent_id not in self.skills_by_agent:
                    self.skills_by_agent[agent_id] = []
                self.skills_by_agent[agent_id].append(skill)

    def _parse_skill(self, data: Dict[str, Any]) -> SkillContract:
        """Parse skill definition from dictionary."""
        input_schema = [
            ParameterDefinition(
                name=param["name"],
                data_type=param.get("data_type", "string"),
                required=param.get("required", True),
                description=param.get("description", ""),
                default_value=param.get("default_value"),
                constraints=param.get("constraints", {}),
            )
            for param in data.get("input_schema", [])
        ]

        output_schema = [
            ParameterDefinition(
                name=param["name"],
                data_type=param.get("data_type", "string"),
                description=param.get("description", ""),
                constraints=param.get("constraints", {}),
            )
            for param in data.get("output_schema", [])
        ]

        return SkillContract(
            skill_id=data["id"],
            name=data["name"],
            description=data["description"],
            execution_type=SkillExecutionType(data.get("execution_type", "native")),
            version=data.get("version", "1.0.0"),
            input_schema=input_schema,
            output_schema=output_schema,
            dependencies=data.get("dependencies", []),
            compatible_agents=data.get("compatible_agents", []),
            required_mcps=data.get("required_mcps", []),
            required_brain_context=data.get("required_brain_context", []),
            tags=data.get("tags", []),
            source=data.get("source", ""),
            category=data.get("category", ""),
            author=data.get("author", ""),
            documentation_url=data.get("documentation_url", ""),
        )

    def get_skill(self, skill_id: str) -> Optional[SkillContract]:
        """Get skill by ID."""
        return self.skills.get(skill_id)

    def list_skills(self) -> List[SkillContract]:
        """List all registered skills."""
        return list(self.skills.values())

    def get_skills_by_category(self, category: str) -> List[SkillContract]:
        """Get all skills in a category."""
        return self.skills_by_category.get(category, [])

    def get_skills_for_agent(self, agent_id: str) -> List[SkillContract]:
        """Get all skills available to an agent."""
        return self.skills_by_agent.get(agent_id, [])

    def find_skills_by_tag(self, tag: str) -> List[SkillContract]:
        """Find skills by tag."""
        return [skill for skill in self.skills.values() if tag in skill.tags]

    def find_skills_by_execution_type(self, execution_type: SkillExecutionType) -> List[SkillContract]:
        """Find skills by execution type."""
        return [skill for skill in self.skills.values() if skill.execution_type == execution_type]

    def validate_skill_chain(self, skill_ids: List[str]) -> tuple[bool, Optional[str]]:
        """Validate that skills can be chained together.

        Checks dependencies and output/input compatibility.
        """
        if not skill_ids:
            return True, None

        # Get all skills
        skills_to_chain = [self.get_skill(skill_id) for skill_id in skill_ids]
        if None in skills_to_chain:
            missing = [skill_ids[i] for i, s in enumerate(skills_to_chain) if s is None]
            return False, f"Unknown skills: {missing}"

        # Check dependencies
        for skill in skills_to_chain:
            for dep_id in skill.dependencies:
                if dep_id not in skill_ids:
                    return False, f"Skill {skill.skill_id} requires {dep_id} which is not in the chain"

        return True, None

    def to_dict(self) -> Dict[str, Any]:
        """Export registry as dictionary."""
        return {
            "skills": {skill_id: self._skill_to_dict(skill) for skill_id, skill in self.skills.items()},
            "categories": self.skills_by_category,
        }

    def _skill_to_dict(self, skill: SkillContract) -> Dict[str, Any]:
        """Convert skill to dictionary."""
        return {
            "id": skill.skill_id,
            "name": skill.name,
            "description": skill.description,
            "execution_type": skill.execution_type.value,
            "version": skill.version,
            "category": skill.category,
            "tags": skill.tags,
        }

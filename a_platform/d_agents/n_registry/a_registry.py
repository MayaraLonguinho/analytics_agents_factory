"""Agent Registry - Central registry for all agents.

Manages agent discovery, contract validation, and orchestration.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from a_platform.a_core.a_contracts.a_agent_contract import AgentContract, AgentCapability


class AgentRegistry:
    """Registry for managing and accessing agents."""

    def __init__(self, agents_root: Optional[Path] = None):
        if agents_root is None:
            self.agents_root = Path(__file__).resolve().parents[1] / "c_agents"
        else:
            self.agents_root = Path(agents_root).resolve()

        self.agents: Dict[str, AgentContract] = {}
        self.agents_by_responsibility: Dict[str, AgentContract] = {}
        self._load_agents()

    def _load_agents(self) -> None:
        """Load agent declarations from YAML."""
        declarations_file = self.agents_root / "declarations" / "agents.yaml"
        if not declarations_file.exists():
            return

        with declarations_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        for agent_data in data.get("agents", []):
            agent = self._parse_agent(agent_data)
            self.agents[agent.agent_id] = agent

            # Index by responsibility
            if agent.responsibility:
                self.agents_by_responsibility[agent.responsibility] = agent

    def _parse_agent(self, data: Dict[str, Any]) -> AgentContract:
        """Parse agent definition from dictionary."""
        capabilities = [
            AgentCapability(
                skill_id=cap.get("skill_id", ""),
                skill_name=cap.get("skill_name", ""),
                description=cap.get("description", ""),
            )
            for cap in data.get("capabilities", [])
        ]

        return AgentContract(
            agent_id=data["id"],
            name=data["name"],
            description=data["description"],
            responsibility=data.get("responsibility", ""),
            input_schema=data.get("input_schema", {}),
            output_schema=data.get("output_schema", {}),
            allowed_skills=data.get("allowed_skills", []),
            allowed_mcps=data.get("allowed_mcps", []),
            applicable_rules=data.get("applicable_rules", []),
            required_context=data.get("required_context", []),
            capabilities=capabilities,
            version=data.get("version", "1.0.0"),
            tags=data.get("tags", []),
        )

    def get_agent(self, agent_id: str) -> Optional[AgentContract]:
        """Get agent by ID."""
        return self.agents.get(agent_id)

    def list_agents(self) -> List[AgentContract]:
        """List all registered agents."""
        return list(self.agents.values())

    def get_agent_by_responsibility(self, responsibility: str) -> Optional[AgentContract]:
        """Get agent by responsibility."""
        return self.agents_by_responsibility.get(responsibility)

    def find_agents_by_tag(self, tag: str) -> List[AgentContract]:
        """Find agents by tag."""
        return [agent for agent in self.agents.values() if tag in agent.tags]

    def validate_agent_contract(self, agent_id: str) -> tuple[bool, Optional[str]]:
        """Validate an agent's contract."""
        agent = self.get_agent(agent_id)
        if not agent:
            return False, f"Agent {agent_id} not found"

        # Validate required fields
        if not agent.agent_id or not agent.name or not agent.responsibility:
            return False, "Agent must have id, name, and responsibility"

        # Validate allowed_skills exist
        # This would require skill registry reference
        # TODO: Add skill registry validation

        return True, None

    def to_dict(self) -> Dict[str, Any]:
        """Export registry as dictionary."""
        return {
            "agents": {agent_id: self._agent_to_dict(agent) for agent_id, agent in self.agents.items()},
            "by_responsibility": {
                resp: agent.agent_id for resp, agent in self.agents_by_responsibility.items()
            },
        }

    def _agent_to_dict(self, agent: AgentContract) -> Dict[str, Any]:
        """Convert agent to dictionary."""
        return {
            "id": agent.agent_id,
            "name": agent.name,
            "description": agent.description,
            "responsibility": agent.responsibility,
            "version": agent.version,
            "tags": agent.tags,
            "allowed_skills": agent.allowed_skills,
            "applicable_rules": agent.applicable_rules,
        }

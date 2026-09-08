"""Base Agent Contract - Defines agent interface and responsibilities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentCapability:
    """Represents a capability an agent can perform."""

    skill_id: str
    skill_name: str
    description: str


@dataclass
class AgentContract:
    """Contract defining an agent's interface and responsibilities."""

    agent_id: str
    name: str
    description: str
    responsibility: str  # Primary responsibility
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    allowed_skills: List[str] = field(default_factory=list)
    allowed_mcps: List[str] = field(default_factory=list)
    applicable_rules: List[str] = field(default_factory=list)
    required_context: List[str] = field(default_factory=list)  # Context types needed
    capabilities: List[AgentCapability] = field(default_factory=list)
    version: str = "1.0.0"
    tags: List[str] = field(default_factory=list)


class IAgent(ABC):
    """Interface for all agents."""

    @abstractmethod
    def get_contract(self) -> AgentContract:
        """Get agent contract defining responsibilities and interface."""
        pass

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent's primary responsibility.

        Args:
            input_data: Input according to contract input_schema

        Returns:
            Output according to contract output_schema
        """
        pass

    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input against contract schema."""
        pass

    @abstractmethod
    def get_required_skills(self) -> List[str]:
        """Get list of skills required by this agent."""
        pass


class BaseAgent(IAgent):
    """Base implementation for all agents.

    Provides common functionality:
    - Contract management
    - Input validation
    - Skill coordination
    - Rule enforcement
    - Brain integration
    """

    def __init__(self, brain_registry: Optional[Any] = None):
        """Initialize agent with optional Brain registry.

        Args:
            brain_registry: Reference to central Brain for rules/knowledge
        """
        self.brain_registry = brain_registry

    def get_contract(self) -> AgentContract:
        """Return agent contract. Should be overridden by subclasses."""
        raise NotImplementedError("Subclass must implement get_contract()")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent logic. Should be overridden by subclasses."""
        raise NotImplementedError("Subclass must implement execute()")

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input against contract schema."""
        contract = self.get_contract()
        if not contract.input_schema:
            return True

        required_fields = set(contract.input_schema.get("required", []))
        provided_fields = set(input_data.keys())

        return required_fields.issubset(provided_fields)

    def get_required_skills(self) -> List[str]:
        """Get list of required skills."""
        contract = self.get_contract()
        return contract.allowed_skills

    def get_applicable_rules(self) -> List[str]:
        """Get applicable rules from contract."""
        contract = self.get_contract()
        return contract.applicable_rules

    async def coordinate_skill(self, skill_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with a skill. Must implement skill invocation."""
        raise NotImplementedError("Subclass must implement coordinate_skill()")

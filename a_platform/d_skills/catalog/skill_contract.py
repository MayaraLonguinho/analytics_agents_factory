"""Base Skill Contract - Defines skill interface and execution model."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class SkillExecutionType(str, Enum):
    """Skill execution type."""

    NATIVE = "native"  # Python/native implementation
    LLM = "llm"  # Uses Language Model
    MCP = "mcp"  # Uses Model Context Protocol
    COMPOSITE = "composite"  # Combines multiple skills


@dataclass
class ParameterDefinition:
    """Definition of a parameter (input or output)."""

    name: str
    data_type: str  # string, integer, float, boolean, list, dict, object
    required: bool = True
    description: str = ""
    default_value: Optional[Any] = None
    constraints: Dict[str, Any] = field(default_factory=dict)  # min, max, pattern, etc


@dataclass
class SkillContract:
    """Contract defining a skill's interface and execution model."""

    skill_id: str
    name: str
    description: str
    execution_type: SkillExecutionType
    version: str = "1.0.0"
    input_schema: List[ParameterDefinition] = field(default_factory=list)
    output_schema: List[ParameterDefinition] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # Skill IDs
    compatible_agents: List[str] = field(default_factory=list)  # Agent IDs
    required_mcps: List[str] = field(default_factory=list)
    required_brain_context: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    source: str = ""  # Where the skill is implemented
    category: str = ""  # discovery, dataset, analytics, data_engineering, development, quality
    author: str = ""
    documentation_url: str = ""


class ISkill(ABC):
    """Interface for all skills."""

    @abstractmethod
    def get_contract(self) -> SkillContract:
        """Get skill contract defining interface and execution model."""
        pass

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the skill.

        Args:
            input_data: Input according to contract input_schema

        Returns:
            Output according to contract output_schema
        """
        pass

    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate input against contract schema.

        Returns:
            (is_valid, error_message)
        """
        pass


class BaseSkill(ISkill):
    """Base implementation for all skills.

    Provides common functionality:
    - Contract management
    - Input/output validation
    - Execution handling
    - Error handling
    """

    def __init__(self, brain_registry: Optional[Any] = None):
        """Initialize skill with optional Brain registry.

        Args:
            brain_registry: Reference to central Brain for rules/knowledge
        """
        self.brain_registry = brain_registry

    def get_contract(self) -> SkillContract:
        """Return skill contract. Should be overridden by subclasses."""
        raise NotImplementedError("Subclass must implement get_contract()")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute skill. Should be overridden by subclasses."""
        raise NotImplementedError("Subclass must implement execute()")

    def validate_input(self, input_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate input against contract schema."""
        contract = self.get_contract()

        # Check required fields
        for param in contract.input_schema:
            if param.required and param.name not in input_data:
                return False, f"Required parameter '{param.name}' is missing"

            if param.name in input_data:
                value = input_data[param.name]

                # Type validation
                expected_type = param.data_type
                if not self._validate_type(value, expected_type):
                    return False, f"Parameter '{param.name}' has incorrect type (expected {expected_type})"

                # Constraint validation
                if param.constraints:
                    is_valid, error = self._validate_constraints(value, param.constraints)
                    if not is_valid:
                        return False, f"Parameter '{param.name}' constraint violation: {error}"

        return True, None

    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """Validate value type."""
        type_map = {
            "string": str,
            "integer": int,
            "float": (int, float),
            "boolean": bool,
            "list": list,
            "dict": dict,
            "object": dict,
        }

        if expected_type == "any":
            return True

        expected_python_type = type_map.get(expected_type)
        if expected_python_type is None:
            return True  # Unknown type, skip validation

        return isinstance(value, expected_python_type)

    def _validate_constraints(self, value: Any, constraints: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate value against constraints."""
        for constraint_type, constraint_value in constraints.items():
            if constraint_type == "min" and isinstance(value, (int, float)):
                if value < constraint_value:
                    return False, f"Value {value} is below minimum {constraint_value}"

            elif constraint_type == "max" and isinstance(value, (int, float)):
                if value > constraint_value:
                    return False, f"Value {value} is above maximum {constraint_value}"

            elif constraint_type == "pattern" and isinstance(value, str):
                import re
                if not re.match(constraint_value, value):
                    return False, f"Value '{value}' does not match pattern {constraint_value}"

            elif constraint_type == "enum" and isinstance(constraint_value, list):
                if value not in constraint_value:
                    return False, f"Value '{value}' is not in allowed values {constraint_value}"

        return True, None

"""Rule Registry - Manage and access Brain rules.

Provides rule validation, enforcement, and querying.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .knowledge_registry import BrainRegistry


class RuleRegistry:
    """Registry for managing and querying rules."""

    def __init__(self, registry: BrainRegistry):
        self.registry = registry

    def get_rule(self, rule_id: str) -> Optional[Any]:
        """Get a rule by ID."""
        return self.registry.get_rule(rule_id)

    def get_applicable_rules(self, applies_to: str) -> List[Any]:
        """Get all rules applicable to a context."""
        return [r for r in self.registry.state.rules.values() if applies_to in r.applies_to]

    def get_rules_by_severity(self, severity: str) -> List[Any]:
        """Get rules by severity."""
        return self.registry.get_rules_by_severity(severity)

    def validate_against_rules(self, element: Dict[str, Any], applicable_rules: List[Any]) -> Dict[str, Any]:
        """Validate an element against rules."""
        violations = []
        warnings = []

        for rule in applicable_rules:
            # Placeholder for rule validation logic
            # Each rule type would have specific validation logic
            pass

        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
        }

    def get_critical_rules(self) -> List[Any]:
        """Get all critical-severity rules."""
        return self.registry.get_rules_by_severity("critical")

    def enforce_rule(self, rule_id: str, context: Dict[str, Any]) -> bool:
        """Check if a rule is enforced in a given context."""
        rule = self.get_rule(rule_id)
        if not rule:
            return True

        # Placeholder for rule enforcement logic
        return True

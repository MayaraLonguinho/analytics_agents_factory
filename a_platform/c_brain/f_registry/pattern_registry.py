"""Pattern Registry - Manage and access Brain patterns.

Provides pattern recommendations, implementation guidance, and querying.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .knowledge_registry import BrainRegistry


class PatternRegistry:
    """Registry for managing and querying patterns."""

    def __init__(self, registry: BrainRegistry):
        self.registry = registry

    def get_pattern(self, pattern_id: str) -> Optional[Any]:
        """Get a pattern by ID."""
        return self.registry.get_pattern(pattern_id)

    def get_applicable_patterns(self, applies_to: str) -> List[Any]:
        """Get all patterns applicable to a context."""
        return [p for p in self.registry.state.patterns.values() if applies_to in p.applies_to]

    def get_patterns_by_tag(self, tag: str) -> List[Any]:
        """Get patterns by tag."""
        return self.registry.get_patterns_by_tag(tag)

    def recommend_patterns(self, domain_id: str) -> List[Any]:
        """Recommend patterns for a domain."""
        return self.registry.get_patterns_for_domain(domain_id)

    def get_implementation_guide(self, pattern_id: str) -> Dict[str, Any]:
        """Get implementation guide for a pattern."""
        pattern = self.get_pattern(pattern_id)
        if not pattern:
            return {}

        return {
            "pattern_id": pattern_id,
            "name": pattern.name,
            "description": pattern.description,
            "components": pattern.components,
            "applicable_to": pattern.applies_to,
            "tags": pattern.tags,
            "source": pattern.source,
            "version": pattern.version,
        }

    def get_pattern_relationships(self, pattern_id: str) -> Dict[str, List[Any]]:
        """Get relationships of a pattern."""
        pattern = self.get_pattern(pattern_id)
        if not pattern:
            return {}

        related = self.registry.graph.find_related(pattern_id, depth=2)

        return {
            "related_patterns": [self.registry.state.patterns.get(id) for id in related if id in self.registry.state.patterns],
            "related_rules": [self.registry.state.rules.get(id) for id in related if id in self.registry.state.rules],
            "related_knowledge": [self.registry.state.knowledge.get(id) for id in related if id in self.registry.state.knowledge],
        }

"""Brain Registry - Unified access to Brain knowledge, rules, patterns, and domains.

Provides query and access interfaces for agents, discovery, planner, and other components.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .brain_loader import BrainLoader, BrainState
from .graph_builder import KnowledgeGraphBuilder


class BrainRegistry:
    """Unified registry for accessing Brain elements."""

    def __init__(self, brain_root: Optional[Path] = None):
        self.loader = BrainLoader(brain_root)
        self.state = self.loader.load()
        self.graph = KnowledgeGraphBuilder(self.state).build()

    # Knowledge Access
    def get_knowledge(self, knowledge_id: str) -> Optional[Any]:
        """Get knowledge by ID."""
        return self.state.get_knowledge(knowledge_id)

    def find_knowledge_by_tag(self, tag: str) -> List[Any]:
        """Find all knowledge with a specific tag."""
        return [k for k in self.state.knowledge.values() if tag in k.tags]

    def find_knowledge_by_type(self, knowledge_type: str) -> List[Any]:
        """Find all knowledge of a specific type."""
        return [k for k in self.state.knowledge.values() if k.type == knowledge_type]

    # Rule Access
    def get_rule(self, rule_id: str) -> Optional[Any]:
        """Get rule by ID."""
        return self.state.get_rule(rule_id)

    def get_rules_for_domain(self, domain_id: str) -> List[Any]:
        """Get all rules applicable to a domain."""
        return self.state.get_domain_rules(domain_id)

    def get_rules_by_severity(self, severity: str) -> List[Any]:
        """Get rules by severity level."""
        return [r for r in self.state.rules.values() if r.severity == severity]

    def get_rules_by_tag(self, tag: str) -> List[Any]:
        """Get rules by tag."""
        return [r for r in self.state.rules.values() if tag in r.tags]

    # Pattern Access
    def get_pattern(self, pattern_id: str) -> Optional[Any]:
        """Get pattern by ID."""
        return self.state.get_pattern(pattern_id)

    def get_patterns_for_domain(self, domain_id: str) -> List[Any]:
        """Get all patterns applicable to a domain."""
        return self.state.get_domain_patterns(domain_id)

    def get_patterns_by_tag(self, tag: str) -> List[Any]:
        """Get patterns by tag."""
        return [p for p in self.state.patterns.values() if tag in p.tags]

    # Domain Access
    def get_domain(self, domain_id: str) -> Optional[Any]:
        """Get domain by ID."""
        return self.state.get_domain(domain_id)

    def list_domains(self) -> List[Any]:
        """List all available domains."""
        return list(self.state.domains.values())

    def get_domain_architecture(self, domain_id: str) -> Dict[str, str]:
        """Get default architecture for domain."""
        return self.state.get_domain_architecture(domain_id)

    def get_domain_knowledge(self, domain_id: str) -> List[Any]:
        """Get knowledge for a domain."""
        return self.state.get_domain_knowledge(domain_id)

    def find_domain_by_tag(self, tag: str) -> List[Any]:
        """Find domains by tag."""
        return [d for d in self.state.domains.values() if tag in d.tags]

    # Skills
    def get_domain_skills(self, domain_id: str) -> List[str]:
        """Get skills for a domain."""
        return self.state.skill_mappings.get(domain_id, [])

    # Recommendations
    def recommend_architecture(self, domain_id: str, preferences: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Recommend architecture for domain."""
        architecture = self.get_domain_architecture(domain_id)

        if preferences:
            for key, value in preferences.items():
                if key in architecture:
                    architecture[key] = value

        return architecture

    def recommend_rules(self, domain_id: str) -> List[Any]:
        """Recommend rules for domain."""
        return self.get_rules_for_domain(domain_id)

    def recommend_patterns(self, domain_id: str) -> List[Any]:
        """Recommend patterns for domain."""
        return self.get_patterns_for_domain(domain_id)

    # Graph Navigation
    def get_related_knowledge(self, knowledge_id: str) -> List[Any]:
        """Get knowledge related to a specific knowledge element."""
        related_ids = self.graph.find_related(knowledge_id, depth=2)
        return [self.state.knowledge.get(id) for id in related_ids if id in self.state.knowledge]

    def find_path(self, source_id: str, target_id: str) -> Optional[List[str]]:
        """Find relationship path between two elements."""
        return self.graph.find_path(source_id, target_id)

    def get_domain_graph(self, domain_id: str) -> Dict[str, Any]:
        """Get knowledge graph for a domain."""
        return self.graph.get_domain_graph(domain_id)

    # Export
    def export_to_obsidian(self, output_dir: Path) -> None:
        """Export Brain to Obsidian-compatible format."""
        self.graph.export_obsidian_format(output_dir)

    def to_dict(self) -> Dict[str, Any]:
        """Export complete Brain state as dictionary."""
        return self.state.to_dict()


class BrainQueryBuilder:
    """Builder for complex Brain queries."""

    def __init__(self, registry: BrainRegistry):
        self.registry = registry
        self.filters = []
        self.element_type: Optional[str] = None

    def where_type(self, element_type: str) -> BrainQueryBuilder:
        """Filter by element type."""
        self.element_type = element_type
        return self

    def where_tag(self, tag: str) -> BrainQueryBuilder:
        """Filter by tag."""
        self.filters.append(lambda e: tag in e.get("tags", []))
        return self

    def where_domain(self, domain_id: str) -> BrainQueryBuilder:
        """Filter by domain applicability."""
        # Store domain for later filtering
        self.filters.append(lambda e, d=domain_id: d in e.get("applies_to", []))
        return self

    def execute(self) -> List[Any]:
        """Execute query and return results."""
        if self.element_type == "knowledge":
            results = list(self.registry.state.knowledge.values())
        elif self.element_type == "rule":
            results = list(self.registry.state.rules.values())
        elif self.element_type == "pattern":
            results = list(self.registry.state.patterns.values())
        elif self.element_type == "domain":
            results = list(self.registry.state.domains.values())
        else:
            results = []

        # Apply filters
        for filter_fn in self.filters:
            results = [r for r in results if filter_fn(r.to_dict())]

        return results

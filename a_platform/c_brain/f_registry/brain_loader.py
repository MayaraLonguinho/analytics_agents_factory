"""Brain Loader - Load and initialize Brain from declarative definitions.

Transforms YAML declarations into executable Brain structures.
Manages knowledge, rules, patterns, domains, and context.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class BrainElement:
    """Base class for Brain elements."""

    id: str
    type: str
    name: str
    description: str
    tags: List[str] = field(default_factory=list)
    source: str = ""
    version: str = "1.0.0"
    dependencies: List[str] = field(default_factory=list)
    relationships: List[Dict[str, str]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> BrainElement:
        return cls(
            id=data.get("id", ""),
            type=data.get("type", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            tags=data.get("tags", []),
            source=data.get("source", ""),
            version=data.get("version", "1.0.0"),
            dependencies=data.get("dependencies", []),
            relationships=data.get("relationships", []),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "source": self.source,
            "version": self.version,
            "dependencies": self.dependencies,
            "relationships": self.relationships,
        }


@dataclass
class Knowledge(BrainElement):
    """Knowledge element in the Brain."""

    pass


@dataclass
class Rule(BrainElement):
    """Rule element in the Brain."""

    applies_to: List[str] = field(default_factory=list)
    severity: str = "medium"  # critical, high, medium, low

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Rule:
        element = BrainElement.from_dict(data)
        return cls(
            **element.to_dict(),
            applies_to=data.get("applies_to", []),
            severity=data.get("severity", "medium"),
        )

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({"applies_to": self.applies_to, "severity": self.severity})
        return base


@dataclass
class Pattern(BrainElement):
    """Pattern element in the Brain."""

    applies_to: List[str] = field(default_factory=list)
    components: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Pattern:
        element = BrainElement.from_dict(data)
        return cls(
            **element.to_dict(),
            applies_to=data.get("applies_to", []),
            components=data.get("components", []),
        )

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({"applies_to": self.applies_to, "components": self.components})
        return base


@dataclass
class Domain(BrainElement):
    """Domain element in the Brain."""

    architecture_default: Dict[str, str] = field(default_factory=dict)
    applicable_rules: List[str] = field(default_factory=list)
    applicable_patterns: List[str] = field(default_factory=list)
    applicable_knowledge: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Domain:
        element = BrainElement.from_dict(data)
        return cls(
            **element.to_dict(),
            architecture_default=data.get("architecture_default", {}),
            applicable_rules=data.get("applicable_rules", []),
            applicable_patterns=data.get("applicable_patterns", []),
            applicable_knowledge=data.get("applicable_knowledge", []),
        )

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "architecture_default": self.architecture_default,
                "applicable_rules": self.applicable_rules,
                "applicable_patterns": self.applicable_patterns,
                "applicable_knowledge": self.applicable_knowledge,
            }
        )
        return base


@dataclass
class BrainState:
    """Complete state of the Brain."""

    knowledge: Dict[str, Knowledge] = field(default_factory=dict)
    rules: Dict[str, Rule] = field(default_factory=dict)
    patterns: Dict[str, Pattern] = field(default_factory=dict)
    domains: Dict[str, Domain] = field(default_factory=dict)
    skill_mappings: Dict[str, List[str]] = field(default_factory=dict)

    def get_knowledge(self, knowledge_id: str) -> Optional[Knowledge]:
        return self.knowledge.get(knowledge_id)

    def get_rule(self, rule_id: str) -> Optional[Rule]:
        return self.rules.get(rule_id)

    def get_pattern(self, pattern_id: str) -> Optional[Pattern]:
        return self.patterns.get(pattern_id)

    def get_domain(self, domain_id: str) -> Optional[Domain]:
        return self.domains.get(domain_id)

    def get_domain_rules(self, domain_id: str) -> List[Rule]:
        domain = self.get_domain(domain_id)
        if not domain:
            return []
        return [self.rules[rule_id] for rule_id in domain.applicable_rules if rule_id in self.rules]

    def get_domain_patterns(self, domain_id: str) -> List[Pattern]:
        domain = self.get_domain(domain_id)
        if not domain:
            return []
        return [self.patterns[pattern_id] for pattern_id in domain.applicable_patterns if pattern_id in self.patterns]

    def get_domain_knowledge(self, domain_id: str) -> List[Knowledge]:
        domain = self.get_domain(domain_id)
        if not domain:
            return []
        return [self.knowledge[knowledge_id] for knowledge_id in domain.applicable_knowledge if knowledge_id in self.knowledge]

    def get_domain_architecture(self, domain_id: str) -> Dict[str, str]:
        domain = self.get_domain(domain_id)
        return domain.architecture_default if domain else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "knowledge": {k: v.to_dict() for k, v in self.knowledge.items()},
            "rules": {k: v.to_dict() for k, v in self.rules.items()},
            "patterns": {k: v.to_dict() for k, v in self.patterns.items()},
            "domains": {k: v.to_dict() for k, v in self.domains.items()},
            "skill_mappings": self.skill_mappings,
        }


class BrainLoader:
    """Load Brain from YAML declarations and build executable state."""

    def __init__(self, brain_root: Optional[Path] = None):
        if brain_root is None:
            self.brain_root = Path(__file__).resolve().parents[1]
        else:
            self.brain_root = Path(brain_root).resolve()

        self.declarations_dir = self.brain_root / "declarations"
        self.state = BrainState()

    def load(self) -> BrainState:
        """Load all Brain declarations and return unified state."""
        self._load_knowledge()
        self._load_rules()
        self._load_patterns()
        self._load_domains()
        return self.state

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load YAML file from declarations directory."""
        filepath = self.declarations_dir / filename
        if not filepath.exists():
            return {}

        with filepath.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data or {}

    def _load_knowledge(self) -> None:
        """Load knowledge declarations."""
        data = self._load_yaml("knowledge.yaml")
        for knowledge_data in data.get("knowledge", []):
            knowledge = Knowledge.from_dict(knowledge_data)
            self.state.knowledge[knowledge.id] = knowledge

    def _load_rules(self) -> None:
        """Load rule declarations."""
        data = self._load_yaml("rules.yaml")
        for rule_data in data.get("rules", []):
            rule = Rule.from_dict(rule_data)
            self.state.rules[rule.id] = rule

    def _load_patterns(self) -> None:
        """Load pattern declarations."""
        data = self._load_yaml("patterns.yaml")
        for pattern_data in data.get("patterns", []):
            pattern = Pattern.from_dict(pattern_data)
            self.state.patterns[pattern.id] = pattern

    def _load_domains(self) -> None:
        """Load domain declarations."""
        data = self._load_yaml("domains.yaml")
        for domain_data in data.get("domains", []):
            domain = Domain.from_dict(domain_data)
            self.state.domains[domain.id] = domain

        # Load skill mappings
        self.state.skill_mappings = data.get("skill_mappings", {})

    def save_state(self, filepath: Path) -> None:
        """Save Brain state as JSON for caching/debugging."""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(self.state.to_dict(), f, indent=2)

    def load_state(self, filepath: Path) -> None:
        """Load Brain state from JSON file."""
        if not filepath.exists():
            return

        with filepath.open("r", encoding="utf-8") as f:
            data = json.load(f)
            self._restore_from_dict(data)

    def _restore_from_dict(self, data: Dict[str, Any]) -> None:
        """Restore Brain state from dictionary."""
        for knowledge_data in data.get("knowledge", {}).values():
            knowledge = Knowledge.from_dict(knowledge_data)
            self.state.knowledge[knowledge.id] = knowledge

        for rule_data in data.get("rules", {}).values():
            rule = Rule.from_dict(rule_data)
            self.state.rules[rule.id] = rule

        for pattern_data in data.get("patterns", {}).values():
            pattern = Pattern.from_dict(pattern_data)
            self.state.patterns[pattern.id] = pattern

        for domain_data in data.get("domains", {}).values():
            domain = Domain.from_dict(domain_data)
            self.state.domains[domain.id] = domain

        self.state.skill_mappings = data.get("skill_mappings", {})

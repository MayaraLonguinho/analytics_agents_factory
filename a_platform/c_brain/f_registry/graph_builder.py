"""Knowledge Graph Builder - Build and navigate Brain knowledge graph.

Constructs a knowledge graph from Brain elements and relationships.
Enables graph traversal, queries, and visualization.
Compatible with Obsidian/Graphify navigation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from .brain_loader import BrainLoader, BrainState


@dataclass
class GraphNode:
    """Node in the knowledge graph."""

    id: str
    type: str  # knowledge, rule, pattern, domain, skill, mcp
    name: str
    description: str
    tags: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "metadata": self.metadata,
        }


@dataclass
class GraphEdge:
    """Edge in the knowledge graph."""

    source: str
    target: str
    relationship: str  # references, uses, implements, extends, part_of, produces, documents
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "relationship": self.relationship,
            "metadata": self.metadata,
        }


class KnowledgeGraphBuilder:
    """Build and navigate knowledge graph from Brain state."""

    def __init__(self, brain_state: BrainState):
        self.brain_state = brain_state
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []
        self.adjacency_list: Dict[str, List[str]] = {}
        self.reverse_adjacency: Dict[str, List[str]] = {}

    def build(self) -> KnowledgeGraphBuilder:
        """Build graph from Brain state."""
        self._build_nodes()
        self._build_edges()
        self._build_adjacency_lists()
        return self

    def _build_nodes(self) -> None:
        """Convert Brain elements to graph nodes."""
        # Knowledge nodes
        for knowledge_id, knowledge in self.brain_state.knowledge.items():
            self.nodes[knowledge_id] = GraphNode(
                id=knowledge_id,
                type="knowledge",
                name=knowledge.name,
                description=knowledge.description,
                tags=knowledge.tags,
                metadata={
                    "source": knowledge.source,
                    "version": knowledge.version,
                },
            )

        # Rule nodes
        for rule_id, rule in self.brain_state.rules.items():
            self.nodes[rule_id] = GraphNode(
                id=rule_id,
                type="rule",
                name=rule.name,
                description=rule.description,
                tags=rule.tags,
                metadata={
                    "source": rule.source,
                    "version": rule.version,
                    "severity": rule.severity,
                    "applies_to": rule.applies_to,
                },
            )

        # Pattern nodes
        for pattern_id, pattern in self.brain_state.patterns.items():
            self.nodes[pattern_id] = GraphNode(
                id=pattern_id,
                type="pattern",
                name=pattern.name,
                description=pattern.description,
                tags=pattern.tags,
                metadata={
                    "source": pattern.source,
                    "version": pattern.version,
                    "applies_to": pattern.applies_to,
                    "components": pattern.components,
                },
            )

        # Domain nodes
        for domain_id, domain in self.brain_state.domains.items():
            self.nodes[domain_id] = GraphNode(
                id=domain_id,
                type="domain",
                name=domain.name,
                description=domain.description,
                tags=domain.tags,
                metadata={
                    "source": domain.source,
                    "version": domain.version,
                    "architecture_default": domain.architecture_default,
                },
            )

    def _build_edges(self) -> None:
        """Build edges from element relationships."""
        # Knowledge relationships
        for knowledge in self.brain_state.knowledge.values():
            for rel in knowledge.relationships:
                self.edges.append(
                    GraphEdge(
                        source=knowledge.id,
                        target=rel["target"],
                        relationship=rel["type"],
                    )
                )

        # Rule relationships
        for rule in self.brain_state.rules.values():
            for rel in rule.relationships:
                self.edges.append(
                    GraphEdge(
                        source=rule.id,
                        target=rel["target"],
                        relationship=rel["type"],
                    )
                )

        # Pattern relationships
        for pattern in self.brain_state.patterns.values():
            for rel in pattern.relationships:
                self.edges.append(
                    GraphEdge(
                        source=pattern.id,
                        target=rel["target"],
                        relationship=rel["type"],
                    )
                )

        # Domain relationships
        for domain in self.brain_state.domains.values():
            for rel in domain.relationships:
                self.edges.append(
                    GraphEdge(
                        source=domain.id,
                        target=rel["target"],
                        relationship=rel["type"],
                    )
                )

            # Domain to rules, patterns, knowledge
            for rule_id in domain.applicable_rules:
                if rule_id in self.brain_state.rules:
                    self.edges.append(
                        GraphEdge(
                            source=domain.id,
                            target=rule_id,
                            relationship="applies",
                        )
                    )

            for pattern_id in domain.applicable_patterns:
                if pattern_id in self.brain_state.patterns:
                    self.edges.append(
                        GraphEdge(
                            source=domain.id,
                            target=pattern_id,
                            relationship="uses",
                        )
                    )

            for knowledge_id in domain.applicable_knowledge:
                if knowledge_id in self.brain_state.knowledge:
                    self.edges.append(
                        GraphEdge(
                            source=domain.id,
                            target=knowledge_id,
                            relationship="has_knowledge",
                        )
                    )

    def _build_adjacency_lists(self) -> None:
        """Build adjacency lists for graph traversal."""
        # Forward adjacency (source → target)
        for node_id in self.nodes:
            self.adjacency_list[node_id] = []
            self.reverse_adjacency[node_id] = []

        for edge in self.edges:
            if edge.source in self.adjacency_list:
                self.adjacency_list[edge.source].append(edge.target)
            if edge.target in self.reverse_adjacency:
                self.reverse_adjacency[edge.target].append(edge.source)

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def get_neighbors(self, node_id: str) -> List[str]:
        """Get outgoing neighbors (forward edges)."""
        return self.adjacency_list.get(node_id, [])

    def get_dependents(self, node_id: str) -> List[str]:
        """Get incoming neighbors (reverse edges)."""
        return self.reverse_adjacency.get(node_id, [])

    def find_path(self, source: str, target: str, max_depth: int = 5) -> Optional[List[str]]:
        """Find a path between two nodes (BFS)."""
        if source not in self.nodes or target not in self.nodes:
            return None

        if source == target:
            return [source]

        queue = [(source, [source])]
        visited = {source}
        depth = 0

        while queue and depth < max_depth:
            depth += 1
            next_queue = []

            for node, path in queue:
                for neighbor in self.get_neighbors(node):
                    if neighbor == target:
                        return path + [neighbor]

                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_queue.append((neighbor, path + [neighbor]))

            queue = next_queue

        return None

    def find_related(self, node_id: str, relationship_type: Optional[str] = None, depth: int = 2) -> Set[str]:
        """Find all related nodes within depth."""
        if node_id not in self.nodes:
            return set()

        related = set()
        queue = [(node_id, 0)]
        visited = {node_id}

        while queue:
            current, current_depth = queue.pop(0)

            if current_depth >= depth:
                continue

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    related.add(neighbor)
                    queue.append((neighbor, current_depth + 1))

            for dependent in self.get_dependents(current):
                if dependent not in visited:
                    visited.add(dependent)
                    related.add(dependent)
                    queue.append((dependent, current_depth + 1))

        return related

    def get_domain_graph(self, domain_id: str) -> Dict[str, Any]:
        """Get subgraph for a specific domain."""
        if domain_id not in self.nodes:
            return {}

        domain_node = self.nodes[domain_id]
        related = self.find_related(domain_id, depth=3)

        nodes_dict = {domain_id: domain_node.to_dict()}
        for node_id in related:
            if node_id in self.nodes:
                nodes_dict[node_id] = self.nodes[node_id].to_dict()

        edges_list = [
            edge.to_dict()
            for edge in self.edges
            if (edge.source == domain_id or edge.target == domain_id) or (edge.source in related and edge.target in related)
        ]

        return {
            "domain": domain_node.to_dict(),
            "nodes": nodes_dict,
            "edges": edges_list,
        }

    def export_obsidian_format(self, output_dir: Path) -> None:
        """Export graph in Obsidian-compatible format."""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create index file
        index_content = "# Brain Knowledge Graph\n\n"
        index_content += "## Domains\n\n"

        for domain_id, domain in self.brain_state.domains.items():
            index_content += f"- [{domain.name}]({domain_id}.md)\n"

        (output_dir / "INDEX.md").write_text(index_content, encoding="utf-8")

        # Create node files
        for node_id, node in self.nodes.items():
            content = f"# {node.name}\n\n"
            content += f"**Type**: {node.type}\n\n"
            content += f"**Description**: {node.description}\n\n"
            content += f"**Tags**: {', '.join(node.tags)}\n\n"
            content += f"**ID**: `{node.id}`\n\n"

            # Add metadata
            if node.metadata:
                content += "## Metadata\n\n"
                for key, value in node.metadata.items():
                    content += f"- **{key}**: {value}\n"
                content += "\n"

            # Add related nodes
            neighbors = self.get_neighbors(node_id)
            dependents = self.get_dependents(node_id)

            if neighbors:
                content += "## Related (Outgoing)\n\n"
                for neighbor_id in neighbors:
                    if neighbor_id in self.nodes:
                        neighbor = self.nodes[neighbor_id]
                        content += f"- [[{neighbor_id}|{neighbor.name}]]\n"
                content += "\n"

            if dependents:
                content += "## Related (Incoming)\n\n"
                for dependent_id in dependents:
                    if dependent_id in self.nodes:
                        dependent = self.nodes[dependent_id]
                        content += f"- [[{dependent_id}|{dependent.name}]]\n"
                content += "\n"

            (output_dir / f"{node_id}.md").write_text(content, encoding="utf-8")

    def to_dict(self) -> Dict[str, Any]:
        """Export graph as dictionary."""
        return {
            "nodes": {node_id: node.to_dict() for node_id, node in self.nodes.items()},
            "edges": [edge.to_dict() for edge in self.edges],
        }

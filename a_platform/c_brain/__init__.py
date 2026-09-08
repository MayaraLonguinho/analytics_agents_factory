"""Central Brain for Analytics AI Factory.

The Brain is the cognitive and knowledge nucleus of the Analytics AI Factory.
It provides knowledge, rules, patterns, context, memory, and registry mechanisms
to guide project generation and execution.

Two distinct contexts:
- Platform Context: knowledge about how the Analytics AI Factory works
- Project Context: knowledge specific to the project being created

Consumable by:
- Discovery
- Planner
- Agents
- Factory
- Runtime
- Validation
- Quality
- Learning
"""

from .f_registry.brain_loader import BrainLoader
from .f_registry.graph_builder import KnowledgeGraphBuilder

__all__ = [
    "BrainLoader",
    "KnowledgeGraphBuilder",
]

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

from .j_brain import Brain
from .g_graph.b_graph_builder import GraphBuilder

__all__ = [
    "Brain",
    "GraphBuilder",
]

"""
Dependency Resolver - Resolução de dependências
"""

from typing import List, Dict, Any
from .interfaces import IDependencyResolver
from .schemas import DirectedAcyclicGraph


class DependencyResolver(IDependencyResolver):
    """Implementação de resolução de dependências."""

    async def resolve(self, dag: DirectedAcyclicGraph) -> List[str]:
        """Resolve dependências e retorna ordem de execução."""
        return dag.topological_sort()

    async def detect_conflicts(self, dag: DirectedAcyclicGraph) -> List[Dict[str, Any]]:
        """Detecta conflitos de dependências."""
        conflicts = []

        # Verificar ciclos
        if dag.has_cycle():
            conflicts.append({
                "type": "cycle",
                "message": "Graph contains circular dependencies"
            })

        # Verificar nós isolados
        for node in dag.nodes:
            if not dag.get_dependencies(node) and not dag.get_dependents(node):
                if len(dag.nodes) > 1:
                    conflicts.append({
                        "type": "isolated_node",
                        "node": node,
                        "message": f"Node {node} has no dependencies or dependents"
                    })

        return conflicts

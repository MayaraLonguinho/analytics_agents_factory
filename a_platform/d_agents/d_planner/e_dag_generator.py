"""
DAG Generator - Geração de DAGs de dependências
"""

from typing import List
from .f_interfaces import IDAGGenerator
from .i_schemas import Task, DirectedAcyclicGraph


class DAGGenerator(IDAGGenerator):
    """Implementação de geração de DAGs."""

    async def generate(self, tasks: List[Task]) -> DirectedAcyclicGraph:
        """Gera um DAG a partir de tarefas com dependências."""
        dag = DirectedAcyclicGraph()

        # Adicionar nós
        for task in tasks:
            dag.add_node(task.id)

        # Adicionar arestas baseado em dependências
        for task in tasks:
            for dep_id in task.dependencies:
                dag.add_edge(dep_id, task.id)

        return dag

    async def validate(self, dag: DirectedAcyclicGraph) -> bool:
        """Valida se o grafo é um DAG válido."""
        return not dag.has_cycle()

    async def detect_cycles(self, dag: DirectedAcyclicGraph) -> List[tuple]:
        """Detecta ciclos no grafo."""
        cycles = []
        visited = set()
        recursion_stack = set()
        path = []

        def dfs(node: str) -> bool:
            visited.add(node)
            recursion_stack.add(node)
            path.append(node)

            for neighbor in dag.adjacency_list.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in recursion_stack:
                    # Ciclo encontrado
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(tuple(cycle))
                    return True

            path.pop()
            recursion_stack.remove(node)
            return False

        for node in dag.nodes:
            if node not in visited:
                dfs(node)

        return cycles

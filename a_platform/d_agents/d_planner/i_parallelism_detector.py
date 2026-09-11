"""
Parallelism Detector - Detecção de paralelismo em DAGs
"""

from typing import List, Dict
from .f_interfaces import IParallelismDetector
from .i_schemas import Task, DirectedAcyclicGraph, ParallelGroup


class ParallelismDetector(IParallelismDetector):
    """Implementação de detecção de paralelismo."""

    async def detect(self, dag: DirectedAcyclicGraph, tasks: List[Task]) -> List[ParallelGroup]:
        """Detecta grupos de execução paralela."""
        # Calcular níveis de profundidade
        levels = await self.calculate_levels(dag)

        # Agrupar tarefas por nível
        groups_by_level: Dict[int, List[str]] = {}
        for task_id, level in levels.items():
            if level not in groups_by_level:
                groups_by_level[level] = []
            groups_by_level[level].append(task_id)

        # Criar grupos paralelos
        parallel_groups = []
        for level, task_ids in sorted(groups_by_level.items()):
            if len(task_ids) > 1:
                # Criar mapa de task para estimativas
                task_map = {task.id: task for task in tasks}

                group = ParallelGroup(
                    group_id=f"parallel_group_{level}",
                    level=level,
                    task_ids=task_ids
                )

                # Calcular tempo e custo do grupo
                max_time = 0.0
                total_cost = 0.0
                for task_id in task_ids:
                    task = task_map.get(task_id)
                    if task:
                        max_time = max(max_time, task.estimated_time)
                        total_cost += task.estimated_cost

                group.estimated_total_time = max_time
                group.estimated_total_cost = total_cost

                parallel_groups.append(group)

        return parallel_groups

    async def calculate_levels(self, dag: DirectedAcyclicGraph) -> Dict[str, int]:
        """Calcula o nível de profundidade de cada tarefa no DAG."""
        levels = {}

        # Calcular nível usando BFS reverso
        for node in dag.nodes:
            level = self._calculate_node_level(node, dag, levels)
            levels[node] = level

        return levels

    def _calculate_node_level(self, node: str, dag: DirectedAcyclicGraph, memo: Dict[str, int]) -> int:
        """Calcula nível de um nó recursivamente."""
        if node in memo:
            return memo[node]

        dependencies = dag.get_dependencies(node)

        if not dependencies:
            memo[node] = 0
            return 0

        max_dep_level = 0
        for dep in dependencies:
            dep_level = self._calculate_node_level(dep, dag, memo)
            max_dep_level = max(max_dep_level, dep_level)

        memo[node] = max_dep_level + 1
        return memo[node]

    async def estimate_parallel_speedup(self, parallel_groups: List[ParallelGroup]) -> float:
        """Estima o speedup de execução paralela."""
        if not parallel_groups:
            return 1.0

        # Speedup simples: soma dos ganhos de paralelismo
        total_speedup = 1.0
        for group in parallel_groups:
            if len(group.task_ids) > 1:
                # Speedup ideal = número de tarefas no grupo
                # Speedup real = menor para considerar overhead
                ideal_speedup = len(group.task_ids)
                real_speedup = min(ideal_speedup, 4.0)  # Assumir max 4 threads
                total_speedup *= real_speedup

        return total_speedup

"""
Priority Manager - Gerenciamento de prioridades
"""

from typing import List, Optional
from .interfaces import IPriorityManager
from .schemas import Task, TaskPriority, PlanningContext, DirectedAcyclicGraph


class PriorityManager(IPriorityManager):
    """Implementação de gerenciamento de prioridades."""

    async def assign_priority(self, task: Task, context: Optional[PlanningContext] = None) -> str:
        """Atribui prioridade a uma tarefa."""
        # Se já tem prioridade, manter
        if task.priority != TaskPriority.MEDIUM:
            return task.priority.value

        # Atribuir baseado em tipo de tarefa
        type_priority = {
            "data_collection": TaskPriority.HIGH,
            "validation": TaskPriority.MEDIUM,
            "notification": TaskPriority.LOW
        }

        return type_priority.get(task.task_type.value, TaskPriority.MEDIUM).value

    async def assign_all_priorities(self, tasks: List[Task], context: Optional[PlanningContext] = None) -> List[Task]:
        """Atribui prioridades a todas as tarefas."""
        for task in tasks:
            priority_str = await self.assign_priority(task, context)
            task.priority = TaskPriority(priority_str)
        return tasks

    async def prioritize_critical_path(self, tasks: List[Task], dag: DirectedAcyclicGraph) -> List[Task]:
        """Prioriza tarefas no caminho crítico."""
        # Identificar caminho crítico (caminho mais longo)
        critical_path = self._find_critical_path(dag, tasks)

        # Elevar prioridade de tarefas no caminho crítico
        task_map = {task.id: task for task in tasks}
        for task_id in critical_path:
            if task_id in task_map:
                task = task_map[task_id]
                if task.priority != TaskPriority.CRITICAL:
                    task.priority = TaskPriority.HIGH

        return tasks

    def _find_critical_path(self, dag: DirectedAcyclicGraph, tasks: List[Task]) -> List[str]:
        """Encontra o caminho crítico no DAG."""
        task_map = {task.id: task for task in tasks}

        # Calcular tempo mais longo até cada nó
        longest_time = {node: 0.0 for node in dag.nodes}

        # Topological sort
        try:
            sorted_nodes = dag.topological_sort()
        except ValueError:
            # Se tem ciclo, usar ordem de nós
            sorted_nodes = dag.nodes

        for node in sorted_nodes:
            task = task_map.get(node)
            task_time = task.estimated_time if task else 0.0

            max_dep_time = 0.0
            for dep in dag.get_dependencies(node):
                max_dep_time = max(max_dep_time, longest_time[dep])

            longest_time[node] = max_dep_time + task_time

        # Encontrar nó com tempo máximo
        end_node = max(longest_time.keys(), key=lambda n: longest_time[n])

        # Reconstruir caminho crítico
        critical_path = []
        current = end_node
        while current:
            critical_path.append(current)
            # Encontrar predecessor com maior tempo
            predecessors = dag.get_dependencies(current)
            if not predecessors:
                break
            current = max(predecessors, key=lambda p: longest_time[p])

        critical_path.reverse()
        return critical_path

"""
Utils for Planner Agent
"""

from typing import List, Dict, Any
from .i_schemas import Task


def generate_task_id(prefix: str, counter: int) -> str:
    """Gera um ID único para tarefa."""
    return f"{prefix}_{counter}"


def calculate_critical_path(tasks: List[Task], dependencies: Dict[str, List[str]]) -> List[str]:
    """Calcula o caminho crítico do plano."""
    task_map = {task.id: task for task in tasks}
    longest_time = {task.id: 0.0 for task in tasks}

    # Calcular tempo mais longo até cada nó
    for task in tasks:
        task_time = task.estimated_time
        max_dep_time = 0.0
        for dep in dependencies.get(task.id, []):
            max_dep_time = max(max_dep_time, longest_time.get(dep, 0.0))
        longest_time[task.id] = max_dep_time + task_time

    # Encontrar nó com tempo máximo
    end_node = max(longest_time.keys(), key=lambda n: longest_time[n])

    # Reconstruir caminho
    critical_path = []
    current = end_node
    while current:
        critical_path.append(current)
        predecessors = dependencies.get(current, [])
        if not predecessors:
            break
        current = max(predecessors, key=lambda p: longest_time.get(p, 0.0))

    critical_path.reverse()
    return critical_path

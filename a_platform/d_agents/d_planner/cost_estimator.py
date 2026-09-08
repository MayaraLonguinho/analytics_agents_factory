"""
Cost Estimator - Estimação de custos e tempos
"""

from typing import List, Dict, Optional
from .interfaces import ICostEstimator
from .schemas import Task, PlanningContext, ParallelGroup


class CostEstimator(ICostEstimator):
    """Implementação de estimação de custos."""

    # Custo base por tipo de tarefa (em USD)
    COST_FACTORS = {
        "data_collection": 0.01,
        "data_processing": 0.02,
        "analysis": 0.05,
        "calculation": 0.03,
        "validation": 0.01,
        "reporting": 0.02,
        "notification": 0.005,
        "custom": 0.02
    }

    # Tempo base por tipo de tarefa (em segundos)
    TIME_FACTORS = {
        "data_collection": 10.0,
        "data_processing": 30.0,
        "analysis": 60.0,
        "calculation": 20.0,
        "validation": 15.0,
        "reporting": 25.0,
        "notification": 5.0,
        "custom": 30.0
    }

    async def estimate_task_cost(self, task: Task, context: Optional[PlanningContext] = None) -> float:
        """Estima o custo de uma tarefa."""
        base_cost = self.COST_FACTORS.get(task.task_type.value, 0.02)

        # Ajustar baseado em prioridade
        priority_multiplier = {
            "low": 0.8,
            "medium": 1.0,
            "high": 1.2,
            "critical": 1.5
        }.get(task.priority.value, 1.0)

        estimated_cost = base_cost * priority_multiplier

        # Se já tem custo estimado, usar como base
        if task.estimated_cost > 0:
            estimated_cost = task.estimated_cost

        return estimated_cost

    async def estimate_task_time(self, task: Task, context: Optional[PlanningContext] = None) -> float:
        """Estima o tempo de execução de uma tarefa."""
        base_time = self.TIME_FACTORS.get(task.task_type.value, 30.0)

        # Ajustar baseado em prioridade (tarefas críticas podem ter mais recursos)
        priority_multiplier = {
            "low": 1.2,
            "medium": 1.0,
            "high": 0.8,
            "critical": 0.7
        }.get(task.priority.value, 1.0)

        estimated_time = base_time * priority_multiplier

        # Se já tem tempo estimado, usar como base
        if task.estimated_time > 0:
            estimated_time = task.estimated_time

        return estimated_time

    async def estimate_total_cost(self, tasks: List[Task], context: Optional[PlanningContext] = None) -> float:
        """Estima o custo total de um plano."""
        total_cost = 0.0
        for task in tasks:
            task_cost = await self.estimate_task_cost(task, context)
            total_cost += task_cost
        return total_cost

    async def estimate_total_time(self, tasks: List[Task], parallel_groups: List[ParallelGroup]) -> float:
        """Estima o tempo total considerando paralelismo."""
        if not parallel_groups:
            # Sem paralelismo, soma de todos os tempos
            return sum(task.estimated_time for task in tasks)

        # Com paralelismo, somar tempos de grupos
        total_time = 0.0
        for group in parallel_groups:
            total_time += group.estimated_total_time

        # Adicionar tarefas não em grupos paralelos
        grouped_task_ids = set()
        for group in parallel_groups:
            grouped_task_ids.update(group.task_ids)

        for task in tasks:
            if task.id not in grouped_task_ids:
                total_time += task.estimated_time

        return total_time

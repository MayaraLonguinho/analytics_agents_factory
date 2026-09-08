"""
Planner Agent - Agente especializado em planejamento de execução
"""

import time
from typing import Optional
from .interfaces import IPlanner
from .schemas import (
    Task,
    ExecutionPlan,
    PlanningRequest,
    PlanningResult,
    PlanningContext,
    DirectedAcyclicGraph
)
from .decomposition import TaskDecomposer
from .dag_generator import DAGGenerator
from .dependency_resolver import DependencyResolver
from .parallelism_detector import ParallelismDetector
from .cost_estimator import CostEstimator
from .agent_assigner import AgentAssigner
from .priority_manager import PriorityManager


class PlannerAgent(IPlanner):
    """
    Planner Agent - Responsável por planejar a execução de objetivos.
    Decompõe objetivos em tarefas, gera DAGs, detecta paralelismo e estima custos.
    """

    def __init__(self):
        """Inicializa o Planner Agent."""
        self.decomposer = TaskDecomposer()
        self.dag_generator = DAGGenerator()
        self.dependency_resolver = DependencyResolver()
        self.parallelism_detector = ParallelismDetector()
        self.cost_estimator = CostEstimator()
        self.agent_assigner = AgentAssigner()
        self.priority_manager = PriorityManager()

    async def plan(self, request: PlanningRequest) -> PlanningResult:
        """
        Gera um plano de execução para um objetivo.

        Args:
            request: Solicitação de planejamento

        Returns:
            PlanningResult com o plano gerado
        """
        start_time = time.time()
        errors = []
        warnings = []

        try:
            # Etapa 1: Decompor objetivo em tarefas
            tasks = await self.decomposer.decompose(request.objective, request.context)

            if not tasks:
                errors.append("No tasks generated from objective")
                return PlanningResult(
                    success=False,
                    errors=errors,
                    planning_time=time.time() - start_time
                )

            # Etapa 2: Atribuir prioridades
            tasks = await self.priority_manager.assign_all_priorities(tasks, request.context)

            # Etapa 3: Atribuir agentes
            tasks = await self.agent_assigner.assign_all(tasks, request.context)

            # Etapa 4: Estimar custos e tempos
            for task in tasks:
                task.estimated_cost = await self.cost_estimator.estimate_task_cost(task, request.context)
                task.estimated_time = await self.cost_estimator.estimate_task_time(task, request.context)

            # Etapa 5: Gerar DAG
            dag = await self.dag_generator.generate(tasks)

            # Etapa 6: Validar DAG
            if not await self.dag_generator.validate(dag):
                cycles = await self.dag_generator.detect_cycles(dag)
                errors.append(f"Graph contains cycles: {cycles}")
                return PlanningResult(
                    success=False,
                    errors=errors,
                    planning_time=time.time() - start_time
                )

            # Etapa 7: Detectar conflitos
            conflicts = await self.dependency_resolver.detect_conflicts(dag)
            if conflicts:
                for conflict in conflicts:
                    warnings.append(f"Conflict detected: {conflict['message']}")

            # Etapa 8: Detectar paralelismo
            parallel_groups = await self.parallelism_detector.detect(dag, tasks)

            # Etapa 9: Priorizar caminho crítico
            tasks = await self.priority_manager.prioritize_critical_path(tasks, dag)

            # Etapa 10: Estimar custos e tempo total
            total_cost = await self.cost_estimator.estimate_total_cost(tasks, request.context)
            total_time = await self.cost_estimator.estimate_total_time(tasks, parallel_groups)
            sequential_time = sum(task.estimated_time for task in tasks)

            # Etapa 11: Criar plano de execução
            plan = ExecutionPlan(
                objective=request.objective,
                tasks=tasks,
                dag=dag,
                parallel_groups=parallel_groups,
                total_cost=total_cost,
                total_time=total_time,
                sequential_time=sequential_time,
                agents_used={task.responsible_agent for task in tasks},
                context=request.context.dict() if request.context else {}
            )

            return PlanningResult(
                success=True,
                plan=plan,
                errors=errors,
                warnings=warnings,
                planning_time=time.time() - start_time
            )

        except Exception as e:
            errors.append(f"Planning failed: {str(e)}")
            return PlanningResult(
                success=False,
                errors=errors,
                planning_time=time.time() - start_time
            )

    async def decompose(self, objective: str, context: Optional[PlanningContext] = None) -> list:
        """Decompõe um objetivo em tarefas."""
        return await self.decomposer.decompose(objective, context)

    async def generate_dag(self, tasks: list) -> DirectedAcyclicGraph:
        """Gera um DAG de dependências a partir de tarefas."""
        return await self.dag_generator.generate(tasks)

    async def order_dependencies(self, dag: DirectedAcyclicGraph) -> list:
        """Ordena tarefas baseado em dependências."""
        return await self.dependency_resolver.resolve(dag)

    async def detect_parallelism(self, dag: DirectedAcyclicGraph) -> list:
        """Detecta grupos de tarefas que podem ser executadas em paralelo."""
        return await self.parallelism_detector.detect(dag, [])

    async def estimate_costs(self, tasks: list, context: Optional[PlanningContext] = None) -> dict:
        """Estima custos para as tarefas."""
        costs = {}
        for task in tasks:
            costs[task.id] = await self.cost_estimator.estimate_task_cost(task, context)
        return costs

    async def assign_agents(self, tasks: list, context: Optional[PlanningContext] = None) -> list:
        """Atribui agentes responsáveis às tarefas."""
        return await self.agent_assigner.assign_all(tasks, context)

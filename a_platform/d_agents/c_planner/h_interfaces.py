"""
Planner Agent Interfaces - Interfaces para componentes do Planner Agent
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set, Tuple
from .i_schemas import (
    Task,
    ExecutionPlan,
    DirectedAcyclicGraph,
    ParallelGroup,
    PlanningContext,
    PlanningRequest,
    PlanningResult
)


# ============================================================================
# Base Planner Interface
# ============================================================================

class IPlanner(ABC):
    """
    Interface base para o Planner Agent.
    Define contrato para planejamento de objetivos.
    """

    @abstractmethod
    async def plan(self, request: PlanningRequest) -> PlanningResult:
        """
        Gera um plano de execução para um objetivo.

        Args:
            request: Solicitação de planejamento

        Returns:
            PlanningResult com o plano gerado
        """
        pass

    @abstractmethod
    async def decompose(self, objective: str, context: Optional[PlanningContext] = None) -> List[Task]:
        """
        Decompõe um objetivo em tarefas.

        Args:
            objective: Objetivo a decompor
            context: Contexto adicional

        Returns:
            Lista de tarefas
        """
        pass

    @abstractmethod
    async def generate_dag(self, tasks: List[Task]) -> DirectedAcyclicGraph:
        """
        Gera um DAG de dependências a partir de tarefas.

        Args:
            tasks: Lista de tarefas

        Returns:
            DirectedAcyclicGraph representando dependências
        """
        pass

    @abstractmethod
    async def order_dependencies(self, dag: DirectedAcyclicGraph) -> List[str]:
        """
        Ordena tarefas baseado em dependências (topological sort).

        Args:
            dag: DAG de dependências

        Returns:
            Lista de IDs de tarefas em ordem de execução
        """
        pass

    @abstractmethod
    async def detect_parallelism(self, dag: DirectedAcyclicGraph) -> List[ParallelGroup]:
        """
        Detecta grupos de tarefas que podem ser executadas em paralelo.

        Args:
            dag: DAG de dependências

        Returns:
            Lista de grupos paralelos
        """
        pass

    @abstractmethod
    async def estimate_costs(self, tasks: List[Task], context: Optional[PlanningContext] = None) -> Dict[str, float]:
        """
        Estima custos para as tarefas.

        Args:
            tasks: Lista de tarefas
            context: Contexto adicional

        Returns:
            Dicionário mapeando task_id para custo estimado
        """
        pass

    @abstractmethod
    async def assign_agents(self, tasks: List[Task], context: Optional[PlanningContext] = None) -> List[Task]:
        """
        Atribui agentes responsáveis às tarefas.

        Args:
            tasks: Lista de tarefas
            context: Contexto adicional

        Returns:
            Lista de tarefas com agentes atribuídos
        """
        pass


# ============================================================================
# Task Decomposer Interface
# ============================================================================

class ITaskDecomposer(ABC):
    """
    Interface para decomposição de objetivos em tarefas.
    """

    @abstractmethod
    async def decompose(self, objective: str, context: Optional[PlanningContext] = None) -> List[Task]:
        """
        Decompõe um objetivo em tarefas atômicas.

        Args:
            objective: Objetivo a decompor
            context: Contexto adicional

        Returns:
            Lista de tarefas
        """
        pass

    @abstractmethod
    async def identify_dependencies(self, tasks: List[Task]) -> List[Task]:
        """
        Identifica dependências entre tarefas.

        Args:
            tasks: Lista de tarefas

        Returns:
            Lista de tarefas com dependências preenchidas
        """
        pass

    @abstractmethod
    async def eliminate_duplicates(self, tasks: List[Task]) -> List[Task]:
        """
        Elimina tarefas duplicadas.

        Args:
            tasks: Lista de tarefas

        Returns:
            Lista de tarefas sem duplicatas
        """
        pass


# ============================================================================
# DAG Generator Interface
# ============================================================================

class IDAGGenerator(ABC):
    """
    Interface para geração de DAGs.
    """

    @abstractmethod
    async def generate(self, tasks: List[Task]) -> DirectedAcyclicGraph:
        """
        Gera um DAG a partir de tarefas com dependências.

        Args:
            tasks: Lista de tarefas

        Returns:
            DirectedAcyclicGraph
        """
        pass

    @abstractmethod
    async def validate(self, dag: DirectedAcyclicGraph) -> bool:
        """
        Valida se o grafo é um DAG válido.

        Args:
            dag: Grafo a validar

        Returns:
            True se válido
        """
        pass

    @abstractmethod
    async def detect_cycles(self, dag: DirectedAcyclicGraph) -> List[Tuple[str, str]]:
        """
        Detecta ciclos no grafo.

        Args:
            dag: Grafo a analisar

        Returns:
            Lista de arestas que formam ciclos
        """
        pass


# ============================================================================
# Dependency Resolver Interface
# ============================================================================

class IDependencyResolver(ABC):
    """
    Interface para resolução de dependências.
    """

    @abstractmethod
    async def resolve(self, dag: DirectedAcyclicGraph) -> List[str]:
        """
        Resolve dependências e retorna ordem de execução.

        Args:
            dag: DAG de dependências

        Returns:
            Lista de IDs de tarefas em ordem topológica
        """
        pass

    @abstractmethod
    async def detect_conflicts(self, dag: DirectedAcyclicGraph) -> List[Dict[str, Any]]:
        """
        Detecta conflitos de dependências.

        Args:
            dag: DAG de dependências

        Returns:
            Lista de conflitos detectados
        """
        pass


# ============================================================================
# Parallelism Detector Interface
# ============================================================================

class IParallelismDetector(ABC):
    """
    Interface para detecção de paralelismo.
    """

    @abstractmethod
    async def detect(self, dag: DirectedAcyclicGraph, tasks: List[Task]) -> List[ParallelGroup]:
        """
        Detecta grupos de execução paralela.

        Args:
            dag: DAG de dependências
            tasks: Lista de tarefas

        Returns:
            Lista de grupos paralelos
        """
        pass

    @abstractmethod
    async def calculate_levels(self, dag: DirectedAcyclicGraph) -> Dict[str, int]:
        """
        Calcula o nível de profundidade de cada tarefa no DAG.

        Args:
            dag: DAG de dependências

        Returns:
            Dicionário mapeando task_id para nível
        """
        pass

    @abstractmethod
    async def estimate_parallel_speedup(self, parallel_groups: List[ParallelGroup]) -> float:
        """
        Estima o speedup de execução paralela.

        Args:
            parallel_groups: Lista de grupos paralelos

        Returns:
            Fator de speedup
        """
        pass


# ============================================================================
# Cost Estimator Interface
# ============================================================================

class ICostEstimator(ABC):
    """
    Interface para estimação de custos.
    """

    @abstractmethod
    async def estimate_task_cost(self, task: Task, context: Optional[PlanningContext] = None) -> float:
        """
        Estima o custo de uma tarefa.

        Args:
            task: Tarefa a estimar
            context: Contexto adicional

        Returns:
            Custo estimado
        """
        pass

    @abstractmethod
    async def estimate_task_time(self, task: Task, context: Optional[PlanningContext] = None) -> float:
        """
        Estima o tempo de execução de uma tarefa.

        Args:
            task: Tarefa a estimar
            context: Contexto adicional

        Returns:
            Tempo estimado em segundos
        """
        pass

    @abstractmethod
    async def estimate_total_cost(self, tasks: List[Task], context: Optional[PlanningContext] = None) -> float:
        """
        Estima o custo total de um plano.

        Args:
            tasks: Lista de tarefas
            context: Contexto adicional

        Returns:
            Custo total estimado
        """
        pass

    @abstractmethod
    async def estimate_total_time(self, tasks: List[Task], parallel_groups: List[ParallelGroup]) -> float:
        """
        Estima o tempo total de execução considerando paralelismo.

        Args:
            tasks: Lista de tarefas
            parallel_groups: Grupos paralelos

        Returns:
            Tempo total estimado em segundos
        """
        pass


# ============================================================================
# Agent Assigner Interface
# ============================================================================

class IAgentAssigner(ABC):
    """
    Interface para atribuição de agentes.
    """

    @abstractmethod
    async def assign(self, task: Task, available_agents: List[str], context: Optional[PlanningContext] = None) -> str:
        """
        Atribui um agente a uma tarefa.

        Args:
            task: Tarefa a atribuir
            available_agents: Lista de agentes disponíveis
            context: Contexto adicional

        Returns:
            Nome do agente atribuído
        """
        pass

    @abstractmethod
    async def assign_all(self, tasks: List[Task], context: Optional[PlanningContext] = None) -> List[Task]:
        """
        Atribui agentes a todas as tarefas.

        Args:
            tasks: Lista de tarefas
            context: Contexto adicional

        Returns:
            Lista de tarefas com agentes atribuídos
        """
        pass

    @abstractmethod
    async def balance_load(self, tasks: List[Task], context: Optional[PlanningContext] = None) -> List[Task]:
        """
        Balanceia a carga entre agentes.

        Args:
            tasks: Lista de tarefas
            context: Contexto adicional

        Returns:
            Lista de tarefas com load balanceado
        """
        pass


# ============================================================================
# Priority Manager Interface
# ============================================================================

class IPriorityManager(ABC):
    """
    Interface para gerenciamento de prioridades.
    """

    @abstractmethod
    async def assign_priority(self, task: Task, context: Optional[PlanningContext] = None) -> str:
        """
        Atribui prioridade a uma tarefa.

        Args:
            task: Tarefa a priorizar
            context: Contexto adicional

        Returns:
            Prioridade atribuída
        """
        pass

    @abstractmethod
    async def assign_all_priorities(self, tasks: List[Task], context: Optional[PlanningContext] = None) -> List[Task]:
        """
        Atribui prioridades a todas as tarefas.

        Args:
            tasks: Lista de tarefas
            context: Contexto adicional

        Returns:
            Lista de tarefas com prioridades atribuídas
        """
        pass

    @abstractmethod
    async def prioritize_critical_path(self, tasks: List[Task], dag: DirectedAcyclicGraph) -> List[Task]:
        """
        Prioriza tarefas no caminho crítico.

        Args:
            tasks: Lista de tarefas
            dag: DAG de dependências

        Returns:
            Lista de tarefas com prioridades ajustadas
        """
        pass

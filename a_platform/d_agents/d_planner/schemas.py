"""
Planner Agent Schemas - Modelos Pydantic para tarefas e planos
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, Field, validator


# ============================================================================
# Enums
# ============================================================================

class TaskStatus(str, Enum):
    """Status de uma tarefa"""
    PENDING = "pending"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"


class TaskPriority(str, Enum):
    """Prioridade de uma tarefa"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskType(str, Enum):
    """Tipo de tarefa"""
    ANALYSIS = "analysis"
    DATA_COLLECTION = "data_collection"
    DATA_PROCESSING = "data_processing"
    CALCULATION = "calculation"
    VALIDATION = "validation"
    REPORTING = "reporting"
    NOTIFICATION = "notification"
    CUSTOM = "custom"


# ============================================================================
# Task Schemas
# ============================================================================

class Task(BaseModel):
    """
    Tarefa individual no plano de execução.
    Representa uma unidade atômica de trabalho.
    """
    id: str = Field(..., description="Identificador único da tarefa")
    description: str = Field(..., description="Descrição da tarefa")
    task_type: TaskType = Field(default=TaskType.CUSTOM, description="Tipo da tarefa")
    dependencies: List[str] = Field(default_factory=list, description="Lista de IDs de tarefas dependentes")
    estimated_cost: float = Field(default=0.0, ge=0.0, description="Custo estimado de execução")
    estimated_time: float = Field(default=0.0, ge=0.0, description="Tempo estimado em segundos")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Prioridade da tarefa")
    responsible_agent: str = Field(..., description="Agente responsável pela execução")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Status da tarefa")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadados adicionais")
    input_requirements: Dict[str, Any] = Field(default_factory=dict, description="Requisitos de entrada")
    output_specification: Dict[str, Any] = Field(default_factory=dict, description="Especificação de saída")
    retry_policy: Optional[Dict[str, Any]] = Field(None, description="Política de retry")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp de criação")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp de atualização")

    @validator('id')
    def validate_id(cls, v):
        """Valida ID da tarefa"""
        if not v or not v.strip():
            raise ValueError("Task ID cannot be empty")
        return v.strip()

    @validator('description')
    def validate_description(cls, v):
        """Valida descrição da tarefa"""
        if not v or not v.strip():
            raise ValueError("Task description cannot be empty")
        if len(v) > 2000:
            raise ValueError("Task description cannot exceed 2000 characters")
        return v.strip()

    @validator('estimated_cost')
    def validate_estimated_cost(cls, v):
        """Valida custo estimado"""
        if v < 0:
            raise ValueError("Estimated cost cannot be negative")
        return v

    @validator('estimated_time')
    def validate_estimated_time(cls, v):
        """Valida tempo estimado"""
        if v < 0:
            raise ValueError("Estimated time cannot be negative")
        return v

    @validator('dependencies')
    def validate_dependencies(cls, v):
        """Valida dependências"""
        # Validar que não há dependência circular direta
        if v:
            # Remove duplicatas
            return list(set(v))
        return v

    def is_ready(self, completed_tasks: Set[str]) -> bool:
        """
        Verifica se a tarefa está pronta para execução.

        Args:
            completed_tasks: Conjunto de IDs de tarefas completadas

        Returns:
            True se todas as dependências estão completadas
        """
        return all(dep in completed_tasks for dep in self.dependencies)

    def add_dependency(self, task_id: str) -> None:
        """Adiciona uma dependência à tarefa."""
        if task_id not in self.dependencies:
            self.dependencies.append(task_id)
            self.updated_at = datetime.utcnow()

    def remove_dependency(self, task_id: str) -> None:
        """Remove uma dependência da tarefa."""
        if task_id in self.dependencies:
            self.dependencies.remove(task_id)
            self.updated_at = datetime.utcnow()

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# ============================================================================
# DAG Schemas
# ============================================================================

class DirectedAcyclicGraph(BaseModel):
    """
    Grafo Direcionado Acíclico (DAG) representando dependências entre tarefas.
    """
    nodes: List[str] = Field(default_factory=list, description="Lista de IDs de nós (tarefas)")
    edges: List[Tuple[str, str]] = Field(default_factory=list, description="Lista de arestas (from, to)")
    adjacency_list: Dict[str, List[str]] = Field(default_factory=dict, description="Lista de adjacência")
    reverse_adjacency_list: Dict[str, List[str]] = Field(default_factory=dict, description="Lista de adjacência reversa")

    @validator('edges')
    def validate_edges(cls, v, values):
        """Valida que as arestas referenciam nós existentes."""
        nodes = values.get('nodes', [])
        for from_node, to_node in v:
            if from_node not in nodes:
                raise ValueError(f"Edge from_node '{from_node}' not in nodes")
            if to_node not in nodes:
                raise ValueError(f"Edge to_node '{to_node}' not in nodes")
        return v

    def add_node(self, node_id: str) -> None:
        """Adiciona um nó ao grafo."""
        if node_id not in self.nodes:
            self.nodes.append(node_id)
            self.adjacency_list[node_id] = []
            self.reverse_adjacency_list[node_id] = []

    def add_edge(self, from_node: str, to_node: str) -> None:
        """Adiciona uma aresta ao grafo."""
        if from_node not in self.nodes:
            self.add_node(from_node)
        if to_node not in self.nodes:
            self.add_node(to_node)

        if to_node not in self.adjacency_list[from_node]:
            self.adjacency_list[from_node].append(to_node)
            self.reverse_adjacency_list[to_node].append(from_node)
            self.edges.append((from_node, to_node))

    def get_dependencies(self, node_id: str) -> List[str]:
        """Retorna as dependências de um nó."""
        return self.reverse_adjacency_list.get(node_id, [])

    def get_dependents(self, node_id: str) -> List[str]:
        """Retorna os nós dependentes de um nó."""
        return self.adjacency_list.get(node_id, [])

    def has_cycle(self) -> bool:
        """Verifica se o grafo possui ciclos usando DFS."""
        visited = set()
        recursion_stack = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            recursion_stack.add(node)

            for neighbor in self.adjacency_list.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in recursion_stack:
                    return True

            recursion_stack.remove(node)
            return False

        for node in self.nodes:
            if node not in visited:
                if dfs(node):
                    return True

        return False

    def topological_sort(self) -> List[str]:
        """
        Retorna ordenação topológica dos nós.
        Algoritmo de Kahn.

        Returns:
            Lista de IDs de nós em ordem topológica
        """
        if self.has_cycle():
            raise ValueError("Cannot perform topological sort on graph with cycle")

        # Calcular in-degree de cada nó
        in_degree = {node: 0 for node in self.nodes}
        for from_node, to_node in self.edges:
            in_degree[to_node] += 1

        # Encontrar nós com in-degree 0
        queue = [node for node in self.nodes if in_degree[node] == 0]
        result = []

        while queue:
            node = queue.pop(0)
            result.append(node)

            # Reduzir in-degree dos vizinhos
            for neighbor in self.adjacency_list.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(result) != len(self.nodes):
            raise ValueError("Graph has cycle")

        return result


# ============================================================================
# Parallel Group Schemas
# ============================================================================

class ParallelGroup(BaseModel):
    """
    Grupo de tarefas que podem ser executadas em paralelo.
    """
    group_id: str = Field(..., description="ID do grupo")
    level: int = Field(..., description="Nível de profundidade no DAG")
    task_ids: List[str] = Field(default_factory=list, description="IDs das tarefas no grupo")
    estimated_total_time: float = Field(default=0.0, description="Tempo estimado total (máximo)")
    estimated_total_cost: float = Field(default=0.0, description="Custo estimado total (soma)")

    @validator('level')
    def validate_level(cls, v):
        """Valida nível do grupo"""
        if v < 0:
            raise ValueError("Group level cannot be negative")
        return v

    def add_task(self, task_id: str) -> None:
        """Adiciona uma tarefa ao grupo."""
        if task_id not in self.task_ids:
            self.task_ids.append(task_id)


# ============================================================================
# Cost Estimation Schemas
# ============================================================================

class CostEstimate(BaseModel):
    """Estimativa de custo para uma tarefa ou plano."""
    computation_cost: float = Field(default=0.0, ge=0.0, description="Custo computacional")
    storage_cost: float = Field(default=0.0, ge=0.0, description="Custo de armazenamento")
    network_cost: float = Field(default=0.0, ge=0.0, description="Custo de rede")
    total_cost: float = Field(default=0.0, ge=0.0, description="Custo total")
    currency: str = Field(default="USD", description="Moeda")
    confidence_level: float = Field(default=0.8, ge=0.0, le=1.0, description="Nível de confiança")

    @validator('currency')
    def validate_currency(cls, v):
        """Valida moeda"""
        if not v or len(v) != 3:
            raise ValueError("Currency must be a 3-letter ISO code")
        return v.upper()

    def calculate_total(self) -> None:
        """Calcula o custo total."""
        self.total_cost = self.computation_cost + self.storage_cost + self.network_cost


# ============================================================================
# Execution Plan Schemas
# ============================================================================

class ExecutionPlan(BaseModel):
    """
    Plano de execução completo gerado pelo Planner Agent.
    Contém todas as tarefas, dependências e metadados.
    """
    plan_id: str = Field(default_factory=lambda: str(uuid4()), description="ID único do plano")
    objective: str = Field(..., description="Objetivo original do plano")
    tasks: List[Task] = Field(default_factory=list, description="Lista de tarefas")
    dag: DirectedAcyclicGraph = Field(..., description="DAG de dependências")
    parallel_groups: List[ParallelGroup] = Field(default_factory=list, description="Grupos de execução paralela")
    total_cost: float = Field(default=0.0, ge=0.0, description="Custo total estimado")
    total_time: float = Field(default=0.0, ge=0.0, description="Tempo total estimado (considerando paralelismo)")
    sequential_time: float = Field(default=0.0, ge=0.0, description="Tempo sequencial estimado")
    agents_used: Set[str] = Field(default_factory=set, description="Conjunto de agentes utilizados")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp de criação")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp de atualização")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadados adicionais")
    context: Dict[str, Any] = Field(default_factory=dict, description="Contexto adicional")

    @validator('objective')
    def validate_objective(cls, v):
        """Valida objetivo"""
        if not v or not v.strip():
            raise ValueError("Objective cannot be empty")
        return v.strip()

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Retorna uma tarefa por ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_tasks_by_agent(self, agent: str) -> List[Task]:
        """Retorna todas as tarefas de um agente."""
        return [task for task in self.tasks if task.responsible_agent == agent]

    def get_ready_tasks(self, completed_tasks: Set[str]) -> List[Task]:
        """Retorna tarefas prontas para execução."""
        return [task for task in self.tasks if task.is_ready(completed_tasks)]

    def calculate_statistics(self) -> Dict[str, Any]:
        """Calcula estatísticas do plano."""
        total_tasks = len(self.tasks)
        tasks_by_status = {}
        for task in self.tasks:
            status = task.status.value
            tasks_by_status[status] = tasks_by_status.get(status, 0) + 1

        tasks_by_priority = {}
        for task in self.tasks:
            priority = task.priority.value
            tasks_by_priority[priority] = tasks_by_priority.get(priority, 0) + 1

        tasks_by_agent = {}
        for task in self.tasks:
            agent = task.responsible_agent
            tasks_by_agent[agent] = tasks_by_agent.get(agent, 0) + 1

        return {
            "total_tasks": total_tasks,
            "tasks_by_status": tasks_by_status,
            "tasks_by_priority": tasks_by_priority,
            "tasks_by_agent": tasks_by_agent,
            "total_cost": self.total_cost,
            "total_time": self.total_time,
            "sequential_time": self.sequential_time,
            "parallel_efficiency": self.sequential_time / self.total_time if self.total_time > 0 else 1.0,
            "num_parallel_groups": len(self.parallel_groups)
        }

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            set: lambda v: list(v)
        }


# ============================================================================
# Planning Context Schemas
# ============================================================================

class PlanningContext(BaseModel):
    """Contexto adicional para o planejamento."""
    constraints: Dict[str, Any] = Field(default_factory=dict, description="Restrições (tempo, custo, recursos)")
    available_agents: List[str] = Field(default_factory=list, description="Agentes disponíveis")
    agent_capabilities: Dict[str, List[str]] = Field(default_factory=dict, description="Capacidades dos agentes")
    preferences: Dict[str, Any] = Field(default_factory=dict, description="Preferências de planejamento")
    historical_data: Optional[Dict[str, Any]] = Field(None, description="Dados históricos para estimativas")


class PlanningRequest(BaseModel):
    """Solicitação de planejamento."""
    objective: str = Field(..., description="Objetivo a ser planejado")
    context: Optional[PlanningContext] = Field(None, description="Contexto adicional")
    options: Dict[str, Any] = Field(default_factory=dict, description="Opções de planejamento")


class PlanningResult(BaseModel):
    """Resultado do planejamento."""
    success: bool = Field(..., description="Se o planejamento foi bem-sucedido")
    plan: Optional[ExecutionPlan] = Field(None, description="Plano gerado")
    errors: List[str] = Field(default_factory=list, description="Erros ocorridos")
    warnings: List[str] = Field(default_factory=list, description="Avisos gerados")
    planning_time: float = Field(default=0.0, description="Tempo de planejamento em segundos")

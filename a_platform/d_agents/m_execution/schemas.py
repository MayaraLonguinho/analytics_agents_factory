"""
Schemas do Orchestrator Agent
Define modelos de dados para entrada, saída e estados internos
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class WorkflowStatus(str, Enum):
    """Status possíveis de um workflow"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class AgentExecutionStatus(str, Enum):
    """Status possíveis de execução de um agente"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class OrchestrationInput(BaseModel):
    """
    Modelo de entrada para orquestração.
    Define os dados necessários para iniciar um workflow.
    """
    requirements: str = Field(
        ..., 
        description="Descrição dos requisitos em linguagem natural",
        min_length=10
    )
    project_name: str = Field(
        ..., 
        description="Nome do projeto a ser gerado",
        min_length=1,
        max_length=100
    )
    config: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Configurações adicionais opcionais"
    )
    priority: str = Field(
        default="normal",
        description="Prioridade do workflow (low, normal, high)"
    )
    
    @validator('priority')
    def validate_priority(cls, v):
        allowed_priorities = ["low", "normal", "high"]
        if v not in allowed_priorities:
            raise ValueError(f'Priority must be one of {allowed_priorities}')
        return v


class OrchestrationOutput(BaseModel):
    """
    Modelo de saída da orquestração.
    Contém resultados consolidados de todo o workflow.
    """
    workflow_id: str = Field(..., description="Identificador único do workflow")
    status: WorkflowStatus = Field(..., description="Status final do workflow")
    results: Dict[str, Any] = Field(
        default_factory=dict,
        description="Resultados consolidados de todos os agentes"
    )
    execution_time: float = Field(
        ..., 
        description="Tempo total de execução em segundos"
    )
    agent_executions: List['AgentExecution'] = Field(
        default_factory=list,
        description="Histórico de execuções de cada agente"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Mensagem de erro se o workflow falhou"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp da conclusão"
    )


class AgentExecution(BaseModel):
    """
    Modelo de execução de um agente individual.
    Registra detalhes de cada execução de agente no workflow.
    """
    agent_name: str = Field(..., description="Nome do agente executado")
    status: AgentExecutionStatus = Field(
        ..., 
        description="Status da execução do agente"
    )
    input_data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Dados de entrada para o agente"
    )
    output_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Dados de saída do agente"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Mensagem de erro se a execução falhou"
    )
    execution_time: float = Field(
        ..., 
        description="Tempo de execução em segundos"
    )
    retry_count: int = Field(
        default=0,
        description="Número de tentativas realizadas"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp da execução"
    )


class WorkflowState(BaseModel):
    """
    Modelo de estado interno de um workflow.
    Used for persistence and recovery.
    """
    workflow_id: str = Field(..., description="Identificador único do workflow")
    status: WorkflowStatus = Field(..., description="Status atual do workflow")
    current_agent_index: int = Field(
        default=0,
        description="Índice do agente atual na sequência"
    )
    agent_sequence: List[str] = Field(
        default_factory=list,
        description="Sequência de agentes a executar"
    )
    accumulated_results: Dict[str, Any] = Field(
        default_factory=dict,
        description="Resultados acumulados dos agentes executados"
    )
    agent_executions: List[AgentExecution] = Field(
        default_factory=list,
        description="Histórico de execuções"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Mensagem de erro se ocorreu falha"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp de criação"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp da última atualização"
    )


class WorkflowConfig(BaseModel):
    """
    Modelo de configuração de workflow.
    Define parâmetros de execução do workflow.
    """
    max_concurrent_agents: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Número máximo de agentes em execução concorrente"
    )
    timeout_per_agent: int = Field(
        default=300,
        ge=60,
        description="Timeout em segundos por agente"
    )
    retry_attempts: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Número máximo de tentativas por agente"
    )
    retry_delay: int = Field(
        default=5,
        ge=1,
        description="Delay em segundos entre tentativas"
    )
    continue_on_error: bool = Field(
        default=False,
        description="Continuar execução mesmo com falhas de agentes"
    )
    rollback_on_failure: bool = Field(
        default=True,
        description="Reverter estado em caso de falha crítica"
    )
    notify_on_failure: bool = Field(
        default=True,
        description="Notificar em caso de falha"
    )


class AgentConfig(BaseModel):
    """
    Modelo de configuração de agente individual.
    """
    name: str = Field(..., description="Nome do agente")
    enabled: bool = Field(default=True, description="Se o agente está habilitado")
    timeout: Optional[int] = Field(
        default=None,
        description="Timeout específico para este agente"
    )
    retry_attempts: Optional[int] = Field(
        default=None,
        description="Número de tentativas específico para este agente"
    )
    config: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Configurações adicionais do agente"
    )


class ExecutionPlan(BaseModel):
    """
    Modelo de plano de execução.
    Define a estrutura de execução de um workflow.
    """
    workflow_id: str = Field(..., description="Identificador único do workflow")
    agent_sequence: List[str] = Field(
        default_factory=list,
        description="Sequência de agentes a executar"
    )
    dependencies: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Mapa de dependências entre agentes"
    )
    parallel_groups: List[List[str]] = Field(
        default_factory=list,
        description="Grupos de agentes que podem executar em paralelo"
    )
    estimated_time: float = Field(
        default=0.0,
        description="Tempo estimado de execução em segundos"
    )
    required_inputs: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Inputs requeridos por cada agente"
    )
    config: WorkflowConfig = Field(
        default_factory=WorkflowConfig,
        description="Configuração do workflow"
    )


class ExecutionLog(BaseModel):
    """
    Modelo de log de execução.
    Registra eventos durante execução.
    """
    log_id: str = Field(..., description="Identificador único do log")
    workflow_id: str = Field(..., description="ID do workflow")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp do evento"
    )
    level: str = Field(..., description="Nível de log (INFO, WARNING, ERROR)")
    event_type: str = Field(..., description="Tipo de evento")
    agent_name: Optional[str] = Field(
        default=None,
        description="Nome do agente relacionado"
    )
    message: str = Field(..., description="Mensagem do log")
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Dados adicionais do evento"
    )


class ExecutionStatistics(BaseModel):
    """
    Modelo de estatísticas de execução.
    """
    total_workflows: int = Field(default=0, description="Total de workflows executados")
    successful_workflows: int = Field(default=0, description="Workflows concluídos com sucesso")
    failed_workflows: int = Field(default=0, description="Workflows que falharam")
    total_agent_executions: int = Field(default=0, description="Total de execuções de agentes")
    average_execution_time: float = Field(
        default=0.0,
        description="Tempo médio de execução em segundos"
    )
    agent_success_rate: Dict[str, float] = Field(
        default_factory=dict,
        description="Taxa de sucesso por agente"
    )
    most_failed_agents: List[str] = Field(
        default_factory=list,
        description="Agentes com mais falhas"
    )


class AuditRecord(BaseModel):
    """
    Modelo de registro de auditoria.
    """
    audit_id: str = Field(..., description="Identificador único do registro")
    workflow_id: str = Field(..., description="ID do workflow")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp do evento"
    )
    action: str = Field(..., description="Ação realizada")
    actor: str = Field(..., description="Entidade que realizou a ação")
    target: Optional[str] = Field(default=None, description="Alvo da ação")
    details: Dict[str, Any] = Field(
        default_factory=dict,
        description="Detalhes da ação"
    )
    ip_address: Optional[str] = Field(default=None, description="Endereço IP")
    user_agent: Optional[str] = Field(default=None, description="User agent")


class ContextSnapshot(BaseModel):
    """
    Modelo de snapshot do contexto de execução.
    """
    workflow_id: str = Field(..., description="ID do workflow")
    snapshot_id: str = Field(..., description="ID do snapshot")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp do snapshot"
    )
    context_data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Dados do contexto no momento do snapshot"
    )
    agent_name: Optional[str] = Field(
        default=None,
        description="Agente que gerou o snapshot"
    )


class RetryPolicy(BaseModel):
    """
    Modelo de política de retry.
    """
    max_attempts: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Número máximo de tentativas"
    )
    backoff_factor: float = Field(
        default=2.0,
        ge=1.0,
        description="Fator de backoff exponencial"
    )
    initial_delay: float = Field(
        default=1.0,
        ge=0.0,
        description="Delay inicial em segundos"
    )
    max_delay: float = Field(
        default=60.0,
        ge=0.0,
        description="Delay máximo em segundos"
    )
    retryable_errors: List[str] = Field(
        default_factory=list,
        description="Tipos de erro que podem ser retryados"
    )


class DependencyGraph(BaseModel):
    """
    Modelo de grafo de dependências.
    """
    nodes: List[str] = Field(
        default_factory=list,
        description="Nós do grafo (agentes)"
    )
    edges: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Arestas do grafo (dependências)"
    )
    
    def add_node(self, node: str) -> None:
        """Adiciona um nó ao grafo"""
        if node not in self.nodes:
            self.nodes.append(node)
            self.edges[node] = []
    
    def add_edge(self, from_node: str, to_node: str) -> None:
        """Adiciona uma aresta ao grafo"""
        self.add_node(from_node)
        self.add_node(to_node)
        if to_node not in self.edges[from_node]:
            self.edges[from_node].append(to_node)
    
    def get_dependencies(self, node: str) -> List[str]:
        """Retorna dependências de um nó"""
        return self.edges.get(node, [])
    
    def get_dependents(self, node: str) -> List[str]:
        """Retorna nós que dependem deste nó"""
        dependents = []
        for n, deps in self.edges.items():
            if node in deps:
                dependents.append(n)
        return dependents


# Atualizar forward references
OrchestrationOutput.update_forward_refs()

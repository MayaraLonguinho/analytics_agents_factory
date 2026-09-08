"""
Interfaces do Orchestrator Agent
Define contratos para orquestração de workflows
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .schemas import (
        OrchestrationInput,
        OrchestrationOutput,
        WorkflowStatus,
        AgentExecution,
        WorkflowState,
        WorkflowConfig
    )


class IOrchestrator(ABC):
    """
    Interface principal para orquestração de agentes.
    Define o contrato que o Orchestrator Agent deve implementar.
    """
    
    @abstractmethod
    async def orchestrate_generation(
        self,
        requirements: str,
        project_name: str,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Orquestra o processo completo de geração de aplicação.

        Args:
            requirements: Descrição dos requisitos em linguagem natural
            project_name: Nome do projeto a ser gerado
            config: Configurações adicionais opcional

        Returns:
            Dicionário com resultados da orquestração completa
        """
        pass
    
    @abstractmethod
    async def execute_agent_sequence(
        self, 
        agents: List[str], 
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executa uma sequência de agentes em ordem definida.
        
        Args:
            agents: Lista de nomes de agentes a executar
            input_data: Dados de entrada para o primeiro agente
            
        Returns:
            Dicionário com resultados consolidados de todos os agentes
        """
        pass
    
    @abstractmethod
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """
        Retorna o status atual de um workflow em execução.
        
        Args:
            workflow_id: Identificador único do workflow
            
        Returns:
            Dicionário com status e informações do workflow
        """
        pass
    
    @abstractmethod
    async def cancel_workflow(self, workflow_id: str) -> bool:
        """
        Cancela a execução de um workflow.
        
        Args:
            workflow_id: Identificador único do workflow
            
        Returns:
            True se cancelado com sucesso, False caso contrário
        """
        pass


class IAgentRegistry(ABC):
    """
    Interface para registro e recuperação de agentes.
    """
    
    @abstractmethod
    def register_agent(self, name: str, agent: Any) -> None:
        """
        Registra um agente no sistema.
        
        Args:
            name: Nome único do agente
            agent: Instância do agente
        """
        pass
    
    @abstractmethod
    def get_agent(self, name: str) -> Optional[Any]:
        """
        Recupera um agente pelo nome.
        
        Args:
            name: Nome do agente
            
        Returns:
            Instância do agente ou None se não encontrado
        """
        pass
    
    @abstractmethod
    def list_agents(self) -> List[str]:
        """
        Lista todos os agentes registrados.
        
        Returns:
            Lista de nomes de agentes disponíveis
        """
        pass


class IWorkflowManager(ABC):
    """
    Interface para gestão de workflows.
    """
    
    @abstractmethod
    async def create_workflow(
        self, 
        workflow_id: str, 
        agent_sequence: List[str],
        input_data: Dict[str, Any]
    ) -> None:
        """
        Cria um novo workflow.
        
        Args:
            workflow_id: Identificador único do workflow
            agent_sequence: Sequência de agentes a executar
            input_data: Dados iniciais
        """
        pass
    
    @abstractmethod
    async def update_workflow_status(
        self, 
        workflow_id: str, 
        status: str,
        agent_name: Optional[str] = None,
        result: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Atualiza o status de um workflow.
        
        Args:
            workflow_id: Identificador do workflow
            status: Novo status
            agent_name: Nome do agente atual (opcional)
            result: Resultado parcial (opcional)
        """
        pass
    
    @abstractmethod
    def get_workflow_state(self, workflow_id: str) -> Dict[str, Any]:
        """
        Recupera o estado completo de um workflow.
        
        Args:
            workflow_id: Identificador do workflow
            
        Returns:
            Dicionário com estado completo do workflow
        """
        pass


class IStateManager(ABC):
    """
    Interface para gestão de estado de execução.
    """
    
    @abstractmethod
    def save_state(self, workflow_id: str, state: Dict[str, Any]) -> None:
        """
        Salva o estado de um workflow.
        
        Args:
            workflow_id: Identificador do workflow
            state: Estado a salvar
        """
        pass
    
    @abstractmethod
    def load_state(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Carrega o estado de um workflow.
        
        Args:
            workflow_id: Identificador do workflow
            
        Returns:
            Estado salvo ou None se não encontrado
        """
        pass
    
    @abstractmethod
    def delete_state(self, workflow_id: str) -> None:
        """
        Remove o estado de um workflow.
        
        Args:
            workflow_id: Identificador do workflow
        """
        pass


class IEventBus(ABC):
    """
    Interface para bus de eventos.
    """

    @abstractmethod
    async def publish(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Publica um evento no bus.

        Args:
            event_type: Tipo do evento
            data: Dados do evento
        """
        pass

    @abstractmethod
    async def subscribe(
        self,
        event_type: str,
        callback: Callable
    ) -> None:
        """
        Inscreve um callback para um tipo de evento.

        Args:
            event_type: Tipo do evento
            callback: Função a ser chamada quando o evento ocorrer
        """
        pass


class IPlanner(ABC):
    """
    Interface para planejamento de execução.
    Responsável por interpretar requisitos e construir planos.
    """

    @abstractmethod
    async def create_execution_plan(
        self,
        input_data: OrchestrationInput
    ) -> Dict[str, Any]:
        """
        Cria um plano de execução baseado nos requisitos.

        Args:
            input_data: Dados de entrada da orquestração

        Returns:
            Dicionário com plano de execução (agentes, dependências, ordem)
        """
        pass

    @abstractmethod
    def validate_plan(self, plan: Dict[str, Any]) -> bool:
        """
        Valida se um plano de execução é válido.

        Args:
            plan: Plano de execução a validar

        Returns:
            True se válido, False caso contrário
        """
        pass

    @abstractmethod
    def estimate_execution_time(self, plan: Dict[str, Any]) -> float:
        """
        Estima o tempo de execução de um plano.

        Args:
            plan: Plano de execução

        Returns:
            Tempo estimado em segundos
        """
        pass


class IDispatcher(ABC):
    """
    Interface para despacho de agentes.
    Responsável por executar agentes e gerenciar paralelismo.
    """

    @abstractmethod
    async def dispatch_agent(
        self,
        agent_name: str,
        input_data: Dict[str, Any],
        config: Optional[WorkflowConfig] = None
    ) -> AgentExecution:
        """
        Despacha um agente para execução.

        Args:
            agent_name: Nome do agente a executar
            input_data: Dados de entrada para o agente
            config: Configuração de workflow opcional

        Returns:
            AgentExecution com resultado da execução
        """
        pass

    @abstractmethod
    async def dispatch_parallel(
        self,
        agent_tasks: List[Dict[str, Any]],
        config: Optional[WorkflowConfig] = None
    ) -> List[AgentExecution]:
        """
        Despacha múltiplos agentes em paralelo.

        Args:
            agent_tasks: Lista de tarefas (agent_name, input_data)
            config: Configuração de workflow opcional

        Returns:
            Lista de AgentExecution com resultados
        """
        pass

    @abstractmethod
    async def dispatch_sequence(
        self,
        agent_sequence: List[Dict[str, Any]],
        config: Optional[WorkflowConfig] = None
    ) -> List[AgentExecution]:
        """
        Despacha agentes em sequência.

        Args:
            agent_sequence: Sequência de tarefas
            config: Configuração de workflow opcional

        Returns:
            Lista de AgentExecution com resultados
        """
        pass


class IExecutionLogger(ABC):
    """
    Interface para logging de execução.
    Responsável por registrar logs estruturados e auditoria.
    """

    @abstractmethod
    def log_workflow_start(
        self,
        workflow_id: str,
        input_data: OrchestrationInput
    ) -> None:
        """
        Registra início de workflow.

        Args:
            workflow_id: ID do workflow
            input_data: Dados de entrada
        """
        pass

    @abstractmethod
    def log_workflow_end(
        self,
        workflow_id: str,
        output_data: OrchestrationOutput
    ) -> None:
        """
        Registra fim de workflow.

        Args:
            workflow_id: ID do workflow
            output_data: Dados de saída
        """
        pass

    @abstractmethod
    def log_agent_start(
        self,
        workflow_id: str,
        agent_name: str,
        input_data: Dict[str, Any]
    ) -> None:
        """
        Registra início de execução de agente.

        Args:
            workflow_id: ID do workflow
            agent_name: Nome do agente
            input_data: Dados de entrada
        """
        pass

    @abstractmethod
    def log_agent_end(
        self,
        workflow_id: str,
        agent_name: str,
        execution: AgentExecution
    ) -> None:
        """
        Registra fim de execução de agente.

        Args:
            workflow_id: ID do workflow
            agent_name: Nome do agente
            execution: Dados da execução
        """
        pass

    @abstractmethod
    def log_error(
        self,
        workflow_id: str,
        agent_name: Optional[str],
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Registra erro durante execução.

        Args:
            workflow_id: ID do workflow
            agent_name: Nome do agente (opcional)
            error: Exceção ocorrida
            context: Contexto adicional
        """
        pass

    @abstractmethod
    def get_workflow_logs(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        Recupera logs de um workflow.

        Args:
            workflow_id: ID do workflow

        Returns:
            Lista de logs do workflow
        """
        pass


class IExecutionHistory(ABC):
    """
    Interface para histórico de execuções.
    Responsável por manter registro completo de execuções.
    """

    @abstractmethod
    def record_execution(
        self,
        workflow_id: str,
        execution: AgentExecution
    ) -> None:
        """
        Registra uma execução de agente.

        Args:
            workflow_id: ID do workflow
            execution: Dados da execução
        """
        pass

    @abstractmethod
    def get_workflow_history(self, workflow_id: str) -> List[AgentExecution]:
        """
        Recupera histórico de execuções de um workflow.

        Args:
            workflow_id: ID do workflow

        Returns:
            Lista de execuções do workflow
        """
        pass

    @abstractmethod
    def get_agent_history(
        self,
        agent_name: str,
        limit: int = 100
    ) -> List[AgentExecution]:
        """
        Recupera histórico de execuções de um agente.

        Args:
            agent_name: Nome do agente
            limit: Limite de registros

        Returns:
            Lista de execuções do agente
        """
        pass

    @abstractmethod
    def get_execution_statistics(
        self,
        workflow_id: Optional[str] = None,
        agent_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Recupera estatísticas de execução.

        Args:
            workflow_id: ID do workflow (opcional)
            agent_name: Nome do agente (opcional)

        Returns:
            Dicionário com estatísticas
        """
        pass


class IExecutionContext(ABC):
    """
    Interface para contexto de execução.
    Responsável por manter contexto compartilhado entre agentes.
    """

    @abstractmethod
    def create_context(
        self,
        workflow_id: str,
        input_data: OrchestrationInput
    ) -> None:
        """
        Cria um novo contexto de execução.

        Args:
            workflow_id: ID do workflow
            input_data: Dados de entrada
        """
        pass

    @abstractmethod
    def get_context(self, workflow_id: str) -> Dict[str, Any]:
        """
        Recupera contexto de execução.

        Args:
            workflow_id: ID do workflow

        Returns:
            Dicionário com contexto
        """
        pass

    @abstractmethod
    def update_context(
        self,
        workflow_id: str,
        key: str,
        value: Any
    ) -> None:
        """
        Atualiza um valor no contexto.

        Args:
            workflow_id: ID do workflow
            key: Chave a atualizar
            value: Novo valor
        """
        pass

    @abstractmethod
    def merge_results(
        self,
        workflow_id: str,
        agent_name: str,
        results: Dict[str, Any]
    ) -> None:
        """
        Mescla resultados de agente no contexto.

        Args:
            workflow_id: ID do workflow
            agent_name: Nome do agente
            results: Resultados a mesclar
        """
        pass

    @abstractmethod
    def delete_context(self, workflow_id: str) -> None:
        """
        Remove contexto de execução.

        Args:
            workflow_id: ID do workflow
        """
        pass

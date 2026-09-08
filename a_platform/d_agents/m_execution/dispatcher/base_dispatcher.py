"""
Base Dispatcher - Interface base para dispatchers
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import asyncio
from ...interfaces import IDispatcher
from ...schemas import (
    AgentExecution,
    AgentExecutionStatus,
    WorkflowConfig,
    RetryPolicy
)
from ...utils import (
    should_retry,
    format_error_message,
    calculate_execution_time
)


class BaseDispatcher(IDispatcher, ABC):
    """
    Classe base para dispatchers de agentes.
    Implementa funcionalidades comuns de despacho.
    """

    def __init__(
        self,
        agent_registry: Dict[str, Any],
        default_config: Optional[WorkflowConfig] = None
    ):
        """
        Inicializa o dispatcher.

        Args:
            agent_registry: Registro de agentes disponíveis
            default_config: Configuração padrão de workflow
        """
        self.agent_registry = agent_registry
        self.default_config = default_config or WorkflowConfig()
        self.active_executions: Dict[str, AgentExecution] = {}

    def _get_agent(self, agent_name: str) -> Optional[Any]:
        """
        Recupera um agente do registro.

        Args:
            agent_name: Nome do agente

        Returns:
            Instância do agente ou None
        """
        return self.agent_registry.get(agent_name)

    def _create_retry_policy(
        self,
        config: Optional[WorkflowConfig] = None
    ) -> RetryPolicy:
        """
        Cria política de retry baseada na configuração.

        Args:
            config: Configuração de workflow

        Returns:
            RetryPolicy configurada
        """
        config = config or self.default_config

        return RetryPolicy(
            max_attempts=config.retry_attempts,
            backoff_factor=2.0,
            initial_delay=float(config.retry_delay),
            max_delay=60.0
        )

    async def _execute_with_retry(
        self,
        agent_name: str,
        agent_callable: Callable,
        input_data: Dict[str, Any],
        retry_policy: RetryPolicy
    ) -> AgentExecution:
        """
        Executa agente com política de retry.

        Args:
            agent_name: Nome do agente
            agent_callable: Função callable do agente
            input_data: Dados de entrada
            retry_policy: Política de retry

        Returns:
            AgentExecution com resultado
        """
        retry_count = 0
        last_error = None

        while retry_count <= retry_policy.max_attempts:
            start_time = datetime.utcnow()

            try:
                # Executar agente
                result = await agent_callable(input_data)
                end_time = datetime.utcnow()
                execution_time = calculate_execution_time(start_time, end_time)

                return AgentExecution(
                    agent_name=agent_name,
                    status=AgentExecutionStatus.COMPLETED,
                    input_data=input_data,
                    output_data=result,
                    execution_time=execution_time,
                    retry_count=retry_count,
                    timestamp=start_time
                )

            except Exception as e:
                last_error = e
                end_time = datetime.utcnow()
                execution_time = calculate_execution_time(start_time, end_time)

                # Verificar se deve retry
                if not should_retry(retry_count, retry_policy.max_attempts, e):
                    return AgentExecution(
                        agent_name=agent_name,
                        status=AgentExecutionStatus.FAILED,
                        input_data=input_data,
                        error_message=format_error_message(e),
                        execution_time=execution_time,
                        retry_count=retry_count,
                        timestamp=start_time
                    )

                retry_count += 1

                # Calcular delay com backoff exponencial
                delay = min(
                    retry_policy.initial_delay * (retry_policy.backoff_factor ** (retry_count - 1)),
                    retry_policy.max_delay
                )

                await asyncio.sleep(delay)

        # Todas as tentativas falharam
        return AgentExecution(
            agent_name=agent_name,
            status=AgentExecutionStatus.FAILED,
            input_data=input_data,
            error_message=format_error_message(last_error),
            execution_time=0.0,
            retry_count=retry_count,
            timestamp=datetime.utcnow()
        )

    def _merge_configs(
        self,
        agent_config: Optional[WorkflowConfig],
        workflow_config: Optional[WorkflowConfig]
    ) -> WorkflowConfig:
        """
        Mescla configurações de agente e workflow.

        Args:
            agent_config: Configuração específica do agente
            workflow_config: Configuração do workflow

        Returns:
            WorkflowConfig mesclada
        """
        base_config = self.default_config.dict()

        if workflow_config:
            workflow_dict = workflow_config.dict()
            for key, value in workflow_dict.items():
                if value is not None:
                    base_config[key] = value

        if agent_config:
            agent_dict = agent_config.dict()
            for key, value in agent_dict.items():
                if value is not None:
                    base_config[key] = value

        return WorkflowConfig(**base_config)

    def _track_execution(self, execution: AgentExecution) -> None:
        """
        Rastreia uma execução ativa.

        Args:
            execution: Execução a rastrear
        """
        execution_key = f"{execution.agent_name}_{execution.timestamp.isoformat()}"
        self.active_executions[execution_key] = execution

    def _untrack_execution(self, execution: AgentExecution) -> None:
        """
        Remove rastreamento de uma execução.

        Args:
            execution: Execução a remover
        """
        execution_key = f"{execution.agent_name}_{execution.timestamp.isoformat()}"
        if execution_key in self.active_executions:
            del self.active_executions[execution_key]

    def get_active_executions(self) -> List[AgentExecution]:
        """
        Retorna execuções ativas.

        Returns:
            Lista de execuções ativas
        """
        return list(self.active_executions.values())

    def get_execution_count(self) -> int:
        """
        Retorna número de execuções ativas.

        Returns:
            Número de execuções ativas
        """
        return len(self.active_executions)

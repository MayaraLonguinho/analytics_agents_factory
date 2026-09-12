"""
Agent Dispatcher - Implementação do dispatcher de agentes
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from .b_base_dispatcher import BaseDispatcher
from ...schemas import (
    AgentExecution,
    AgentExecutionStatus,
    WorkflowConfig
)


class AgentDispatcher(BaseDispatcher):
    """
    Implementação do dispatcher de agentes.
    Responsável por executar agentes e gerenciar paralelismo.
    """

    def __init__(
        self,
        agent_registry: Dict[str, Any],
        default_config: Optional[WorkflowConfig] = None
    ):
        """
        Inicializa o AgentDispatcher.

        Args:
            agent_registry: Registro de agentes disponíveis
            default_config: Configuração padrão de workflow
        """
        super().__init__(agent_registry, default_config)
        self.semaphore = asyncio.Semaphore(default_config.max_concurrent_agents if default_config else 5)

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
        # Recuperar agente
        agent = self._get_agent(agent_name)
        if not agent:
            return AgentExecution(
                agent_name=agent_name,
                status=AgentExecutionStatus.FAILED,
                input_data=input_data,
                error_message=f"Agent {agent_name} not found in registry",
                execution_time=0.0,
                retry_count=0,
                timestamp=datetime.utcnow()
            )

        # Mesclar configurações
        merged_config = self._merge_configs(None, config)

        # Criar política de retry
        retry_policy = self._create_retry_policy(merged_config)

        # Determinar callable do agente
        agent_callable = self._get_agent_callable(agent)

        # Executar com retry
        execution = await self._execute_with_retry(
            agent_name,
            agent_callable,
            input_data,
            retry_policy
        )

        return execution

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
        merged_config = self._merge_configs(None, config)
        max_concurrent = merged_config.max_concurrent_agents

        # Criar tarefas assíncronas
        tasks = []
        for task in agent_tasks:
            agent_name = task.get("agent_name")
            input_data = task.get("input_data", {})
            task_config = task.get("config")

            async def dispatch_with_semaphore():
                async with self.semaphore:
                    return await self.dispatch_agent(
                        agent_name,
                        input_data,
                        self._merge_configs(task_config, config)
                    )

            tasks.append(dispatch_with_semaphore())

        # Executar em paralelo com limite de concorrência
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Processar resultados
        executions = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Criar execução falha para exceção
                executions.append(AgentExecution(
                    agent_name=agent_tasks[i].get("agent_name", "unknown"),
                    status=AgentExecutionStatus.FAILED,
                    input_data=agent_tasks[i].get("input_data", {}),
                    error_message=str(result),
                    execution_time=0.0,
                    retry_count=0,
                    timestamp=datetime.utcnow()
                ))
            else:
                executions.append(result)

        return executions

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
        executions = []
        accumulated_results = {}

        for task in agent_sequence:
            agent_name = task.get("agent_name")
            input_data = task.get("input_data", {}).copy()
            task_config = task.get("config")

            # Adicionar resultados acumulados ao input
            input_data.update(accumulated_results)

            # Executar agente
            execution = await self.dispatch_agent(
                agent_name,
                input_data,
                self._merge_configs(task_config, config)
            )

            executions.append(execution)

            # Se falhou e não deve continuar, parar
            merged_config = self._merge_configs(task_config, config)
            if (
                execution.status == AgentExecutionStatus.FAILED
                and not merged_config.continue_on_error
            ):
                # Marcar agentes restantes como skipped
                for remaining_task in agent_sequence[agent_sequence.index(task) + 1:]:
                    executions.append(AgentExecution(
                        agent_name=remaining_task.get("agent_name", "unknown"),
                        status=AgentExecutionStatus.SKIPPED,
                        input_data=remaining_task.get("input_data", {}),
                        error_message="Skipped due to previous failure",
                        execution_time=0.0,
                        retry_count=0,
                        timestamp=datetime.utcnow()
                    ))
                break

            # Acumular resultados se sucesso
            if execution.status == AgentExecutionStatus.COMPLETED and execution.output_data:
                accumulated_results.update(execution.output_data)

        return executions

    def _get_agent_callable(self, agent: Any) -> callable:
        """
        Determina a função callable de um agente.

        Args:
            agent: Instância do agente

        Returns:
            Função callable do agente
        """
        # Tentar diferentes métodos comuns
        if hasattr(agent, 'execute'):
            return agent.execute
        elif hasattr(agent, 'run'):
            return agent.run
        elif hasattr(agent, 'process'):
            return agent.process
        elif hasattr(agent, '__call__'):
            return agent
        else:
            raise AttributeError(
                f"Agent {type(agent).__name__} has no callable method "
                "(execute, run, process, or __call__)"
            )

    async def dispatch_with_dependencies(
        self,
        agent_tasks: List[Dict[str, Any]],
        dependencies: Dict[str, List[str]],
        config: Optional[WorkflowConfig] = None
    ) -> List[AgentExecution]:
        """
        Despacha agentes respeitando dependências.

        Args:
            agent_tasks: Lista de tarefas
            dependencies: Mapa de dependências
            config: Configuração de workflow opcional

        Returns:
            Lista de AgentExecution com resultados
        """
        executions = {}
        results = {}
        remaining = set(task.get("agent_name") for task in agent_tasks)

        while remaining:
            # Encontrar agentes prontos (sem dependências pendentes)
            ready = []
            for agent_name in remaining:
                deps = dependencies.get(agent_name, [])
                if all(dep in results for dep in deps):
                    ready.append(agent_name)

            if not ready:
                # Ciclo detectado ou dependência impossível
                for agent_name in remaining:
                    task = next(t for t in agent_tasks if t.get("agent_name") == agent_name)
                    executions[agent_name] = AgentExecution(
                        agent_name=agent_name,
                        status=AgentExecutionStatus.FAILED,
                        input_data=task.get("input_data", {}),
                        error_message="Dependency cycle or missing dependency",
                        execution_time=0.0,
                        retry_count=0,
                        timestamp=datetime.utcnow()
                    )
                break

            # Executar agentes prontos em paralelo
            ready_tasks = [
                t for t in agent_tasks
                if t.get("agent_name") in ready
            ]

            ready_executions = await self.dispatch_parallel(ready_tasks, config)

            # Processar resultados
            for execution in ready_executions:
                executions[execution.agent_name] = execution
                remaining.discard(execution.agent_name)

                if execution.status == AgentExecutionStatus.COMPLETED and execution.output_data:
                    results[execution.agent_name] = execution.output_data

                # Se falhou e não deve continuar, parar
                merged_config = self._merge_configs(None, config)
                if (
                    execution.status == AgentExecutionStatus.FAILED
                    and not merged_config.continue_on_error
                ):
                    # Marcar restantes como skipped
                    for agent_name in remaining:
                        task = next(t for t in agent_tasks if t.get("agent_name") == agent_name)
                        executions[agent_name] = AgentExecution(
                            agent_name=agent_name,
                            status=AgentExecutionStatus.SKIPPED,
                            input_data=task.get("input_data", {}),
                            error_message="Skipped due to dependency failure",
                            execution_time=0.0,
                            retry_count=0,
                            timestamp=datetime.utcnow()
                        )
                    remaining.clear()

        # Retornar na ordem original
        ordered_executions = []
        for task in agent_tasks:
            agent_name = task.get("agent_name")
            ordered_executions.append(executions[agent_name])

        return ordered_executions

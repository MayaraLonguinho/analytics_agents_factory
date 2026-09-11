"""
Tests for Agent Dispatcher
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, AsyncMock
from ....dispatcher.agent_dispatcher import AgentDispatcher
from ....dispatcher.base_dispatcher import BaseDispatcher
from ....schemas import (
    AgentExecution,
    AgentExecutionStatus,
    WorkflowConfig
)


class MockAgent:
    """Agente mock para testes"""

    def __init__(self, name, should_fail=False):
        self.name = name
        self.should_fail = should_fail

    async def execute(self, input_data):
        """Método execute mock"""
        if self.should_fail:
            raise Exception(f"Agent {self.name} failed")
        return {
            "agent": self.name,
            "result": "success",
            "data": input_data
        }


class TestAgentDispatcher:
    """Testes para AgentDispatcher"""

    @pytest.fixture
    def agent_registry(self):
        """Registro de agentes mock"""
        return {
            "test_agent": MockAgent("test_agent"),
            "failing_agent": MockAgent("failing_agent", should_fail=True)
        }

    @pytest.fixture
    def config(self):
        """Configuração de workflow"""
        return WorkflowConfig(
            max_concurrent_agents=2,
            retry_attempts=2,
            retry_delay=1
        )

    @pytest.fixture
    def dispatcher(self, agent_registry, config):
        """Instância do dispatcher para testes"""
        return AgentDispatcher(agent_registry, config)

    @pytest.mark.asyncio
    async def test_dispatch_agent_success(self, dispatcher):
        """Testa despacho de agente com sucesso"""
        execution = await dispatcher.dispatch_agent(
            "test_agent",
            {"test": "data"}
        )

        assert execution.agent_name == "test_agent"
        assert execution.status == AgentExecutionStatus.COMPLETED
        assert execution.output_data is not None
        assert execution.execution_time > 0

    @pytest.mark.asyncio
    async def test_dispatch_agent_not_found(self, dispatcher):
        """Testa despacho de agente não encontrado"""
        execution = await dispatcher.dispatch_agent(
            "nonexistent_agent",
            {"test": "data"}
        )

        assert execution.agent_name == "nonexistent_agent"
        assert execution.status == AgentExecutionStatus.FAILED
        assert "not found" in execution.error_message.lower()

    @pytest.mark.asyncio
    async def test_dispatch_agent_with_retry(self, dispatcher):
        """Testa despacho de agente com retry"""
        execution = await dispatcher.dispatch_agent(
            "failing_agent",
            {"test": "data"}
        )

        assert execution.agent_name == "failing_agent"
        assert execution.status == AgentExecutionStatus.FAILED
        assert execution.retry_count > 0

    @pytest.mark.asyncio
    async def test_dispatch_parallel(self, dispatcher):
        """Testa despacho paralelo de agentes"""
        # Adicionar mais agentes ao registro
        dispatcher.agent_registry["agent1"] = MockAgent("agent1")
        dispatcher.agent_registry["agent2"] = MockAgent("agent2")
        dispatcher.agent_registry["agent3"] = MockAgent("agent3")

        tasks = [
            {"agent_name": "agent1", "input_data": {"test": "data1"}},
            {"agent_name": "agent2", "input_data": {"test": "data2"}},
            {"agent_name": "agent3", "input_data": {"test": "data3"}}
        ]

        executions = await dispatcher.dispatch_parallel(tasks)

        assert len(executions) == 3
        assert all(e.status == AgentExecutionStatus.COMPLETED for e in executions)

    @pytest.mark.asyncio
    async def test_dispatch_parallel_with_failure(self, dispatcher):
        """Testa despacho paralelo com falha"""
        dispatcher.agent_registry["agent1"] = MockAgent("agent1")
        dispatcher.agent_registry["agent2"] = MockAgent("agent2", should_fail=True)

        tasks = [
            {"agent_name": "agent1", "input_data": {"test": "data1"}},
            {"agent_name": "agent2", "input_data": {"test": "data2"}}
        ]

        executions = await dispatcher.dispatch_parallel(tasks)

        assert len(executions) == 2
        assert executions[0].status == AgentExecutionStatus.COMPLETED
        assert executions[1].status == AgentExecutionStatus.FAILED

    @pytest.mark.asyncio
    async def test_dispatch_sequence(self, dispatcher):
        """Testa despacho sequencial de agentes"""
        dispatcher.agent_registry["agent1"] = MockAgent("agent1")
        dispatcher.agent_registry["agent2"] = MockAgent("agent2")

        sequence = [
            {"agent_name": "agent1", "input_data": {"test": "data1"}},
            {"agent_name": "agent2", "input_data": {"test": "data2"}}
        ]

        executions = await dispatcher.dispatch_sequence(sequence)

        assert len(executions) == 2
        assert all(e.status == AgentExecutionStatus.COMPLETED for e in executions)

    @pytest.mark.asyncio
    async def test_dispatch_sequence_with_failure_continue(self, dispatcher):
        """Testa despacho sequencial com falha e continue_on_error"""
        config = WorkflowConfig(continue_on_error=True)
        dispatcher = AgentDispatcher(dispatcher.agent_registry, config)

        dispatcher.agent_registry["agent1"] = MockAgent("agent1")
        dispatcher.agent_registry["agent2"] = MockAgent("agent2", should_fail=True)
        dispatcher.agent_registry["agent3"] = MockAgent("agent3")

        sequence = [
            {"agent_name": "agent1", "input_data": {"test": "data1"}},
            {"agent_name": "agent2", "input_data": {"test": "data2"}},
            {"agent_name": "agent3", "input_data": {"test": "data3"}}
        ]

        executions = await dispatcher.dispatch_sequence(sequence)

        assert len(executions) == 3
        assert executions[0].status == AgentExecutionStatus.COMPLETED
        assert executions[1].status == AgentExecutionStatus.FAILED
        assert executions[2].status == AgentExecutionStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_dispatch_sequence_with_failure_stop(self, dispatcher):
        """Testa despacho sequencial com falha e stop_on_error"""
        config = WorkflowConfig(continue_on_error=False)
        dispatcher = AgentDispatcher(dispatcher.agent_registry, config)

        dispatcher.agent_registry["agent1"] = MockAgent("agent1")
        dispatcher.agent_registry["agent2"] = MockAgent("agent2", should_fail=True)
        dispatcher.agent_registry["agent3"] = MockAgent("agent3")

        sequence = [
            {"agent_name": "agent1", "input_data": {"test": "data1"}},
            {"agent_name": "agent2", "input_data": {"test": "data2"}},
            {"agent_name": "agent3", "input_data": {"test": "data3"}}
        ]

        executions = await dispatcher.dispatch_sequence(sequence)

        assert len(executions) == 3
        assert executions[0].status == AgentExecutionStatus.COMPLETED
        assert executions[1].status == AgentExecutionStatus.FAILED
        assert executions[2].status == AgentExecutionStatus.SKIPPED

    @pytest.mark.asyncio
    async def test_dispatch_with_dependencies(self, dispatcher):
        """Testa despacho com dependências"""
        dispatcher.agent_registry["agent1"] = MockAgent("agent1")
        dispatcher.agent_registry["agent2"] = MockAgent("agent2")
        dispatcher.agent_registry["agent3"] = MockAgent("agent3")

        tasks = [
            {"agent_name": "agent1", "input_data": {"test": "data1"}},
            {"agent_name": "agent2", "input_data": {"test": "data2"}},
            {"agent_name": "agent3", "input_data": {"test": "data3"}}
        ]

        dependencies = {
            "agent2": ["agent1"],
            "agent3": ["agent2"]
        }

        executions = await dispatcher.dispatch_with_dependencies(tasks, dependencies)

        assert len(executions) == 3
        assert all(e.status == AgentExecutionStatus.COMPLETED for e in executions)

    def test_get_active_executions(self, dispatcher):
        """Testa obtenção de execuções ativas"""
        assert len(dispatcher.get_active_executions()) == 0

    def test_get_execution_count(self, dispatcher):
        """Testa contagem de execuções"""
        assert dispatcher.get_execution_count() == 0


class TestBaseDispatcher:
    """Testes para BaseDispatcher"""

    @pytest.fixture
    def agent_registry(self):
        """Registro de agentes mock"""
        return {
            "test_agent": MockAgent("test_agent")
        }

    @pytest.fixture
    def config(self):
        """Configuração de workflow"""
        return WorkflowConfig()

    @pytest.fixture
    def dispatcher(self, agent_registry, config):
        """Instância do dispatcher base para testes"""
        return BaseDispatcher(agent_registry, config)

    def test_get_agent(self, dispatcher):
        """Testa obtenção de agente"""
        agent = dispatcher._get_agent("test_agent")
        assert agent is not None
        assert agent.name == "test_agent"

    def test_get_agent_not_found(self, dispatcher):
        """Testa obtenção de agente não encontrado"""
        agent = dispatcher._get_agent("nonexistent")
        assert agent is None

    def test_create_retry_policy(self, dispatcher):
        """Testa criação de política de retry"""
        policy = dispatcher._create_retry_policy()

        assert policy.max_attempts > 0
        assert policy.backoff_factor > 0
        assert policy.initial_delay > 0

    def test_merge_configs(self, dispatcher):
        """Testa mesclagem de configurações"""
        agent_config = WorkflowConfig(max_concurrent_agents=3)
        workflow_config = WorkflowConfig(retry_attempts=5)

        merged = dispatcher._merge_configs(agent_config, workflow_config)

        assert merged.max_concurrent_agents == 3
        assert merged.retry_attempts == 5

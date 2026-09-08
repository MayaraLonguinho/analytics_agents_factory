"""
Tests for Workflow Manager
"""

import pytest
from datetime import datetime
from unittest.mock import Mock
from ....workflow_manager.workflow_manager import WorkflowManager
from ....workflow_manager.base_workflow import BaseWorkflowManager
from ....schemas import (
    WorkflowState,
    WorkflowStatus,
    AgentExecution,
    AgentExecutionStatus,
    ExecutionPlan,
    WorkflowConfig
)


class TestWorkflowManager:
    """Testes para WorkflowManager"""

    @pytest.fixture
    def workflow_manager(self):
        """Instância do workflow manager para testes"""
        return WorkflowManager()

    @pytest.fixture
    def sample_plan(self):
        """Plano de execução de exemplo"""
        return ExecutionPlan(
            workflow_id="test-workflow-id",
            agent_sequence=["agent1", "agent2"],
            dependencies={"agent2": ["agent1"]},
            parallel_groups=[["agent1"], ["agent2"]],
            estimated_time=120.0,
            required_inputs={},
            config=WorkflowConfig()
        )

    @pytest.mark.asyncio
    async def test_create_workflow(self, workflow_manager):
        """Testa criação de workflow"""
        await workflow_manager.create_workflow(
            "test-id",
            ["agent1", "agent2"],
            {"test": "data"}
        )

        assert "test-id" in workflow_manager.active_workflows
        state = workflow_manager.active_workflows["test-id"]
        assert state.workflow_id == "test-id"
        assert state.status == WorkflowStatus.PENDING

    @pytest.mark.asyncio
    async def test_update_workflow_status(self, workflow_manager):
        """Testa atualização de status de workflow"""
        await workflow_manager.create_workflow(
            "test-id",
            ["agent1"],
            {}
        )

        await workflow_manager.update_workflow_status(
            "test-id",
            WorkflowStatus.RUNNING
        )

        state = workflow_manager.active_workflows["test-id"]
        assert state.status == WorkflowStatus.RUNNING

    def test_get_workflow_state_active(self, workflow_manager):
        """Testa obtenção de estado de workflow ativo"""
        # Adicionar workflow manualmente
        state = WorkflowState(
            workflow_id="test-id",
            status=WorkflowStatus.RUNNING,
            agent_sequence=["agent1"],
            current_agent_index=0
        )
        workflow_manager.active_workflows["test-id"] = state

        retrieved_state = workflow_manager.get_workflow_state("test-id")

        assert retrieved_state["workflow_id"] == "test-id"
        assert retrieved_state["status"] == WorkflowStatus.RUNNING

    def test_get_workflow_state_not_found(self, workflow_manager):
        """Testa obtenção de estado de workflow não encontrado"""
        with pytest.raises(ValueError, match="not found"):
            workflow_manager.get_workflow_state("nonexistent")

    @pytest.mark.asyncio
    async def test_cancel_workflow(self, workflow_manager):
        """Testa cancelamento de workflow"""
        await workflow_manager.create_workflow(
            "test-id",
            ["agent1"],
            {}
        )

        result = await workflow_manager.cancel_workflow("test-id")

        assert result is True
        assert "test-id" not in workflow_manager.active_workflows
        assert "test-id" in workflow_manager.completed_workflows

    @pytest.mark.asyncio
    async def test_cancel_workflow_not_found(self, workflow_manager):
        """Testa cancelamento de workflow não encontrado"""
        result = await workflow_manager.cancel_workflow("nonexistent")
        assert result is False

    def test_list_active_workflows(self, workflow_manager):
        """Testa listagem de workflows ativos"""
        # Adicionar workflows manualmente
        workflow_manager.active_workflows["id1"] = WorkflowState(
            workflow_id="id1",
            status=WorkflowStatus.RUNNING,
            agent_sequence=[],
            current_agent_index=0
        )
        workflow_manager.active_workflows["id2"] = WorkflowState(
            workflow_id="id2",
            status=WorkflowStatus.RUNNING,
            agent_sequence=[],
            current_agent_index=0
        )

        active = workflow_manager.list_active_workflows()

        assert len(active) == 2
        assert "id1" in active
        assert "id2" in active

    def test_list_completed_workflows(self, workflow_manager):
        """Testa listagem de workflows completados"""
        # Adicionar workflows manualmente
        workflow_manager.completed_workflows["id1"] = WorkflowState(
            workflow_id="id1",
            status=WorkflowStatus.COMPLETED,
            agent_sequence=[],
            current_agent_index=0
        )

        completed = workflow_manager.list_completed_workflows()

        assert len(completed) == 1
        assert "id1" in completed

    def test_get_workflow_statistics(self, workflow_manager):
        """Testa obtenção de estatísticas de workflows"""
        # Adicionar workflows manualmente
        workflow_manager.completed_workflows["id1"] = WorkflowState(
            workflow_id="id1",
            status=WorkflowStatus.COMPLETED,
            agent_sequence=[],
            current_agent_index=0
        )
        workflow_manager.completed_workflows["id2"] = WorkflowState(
            workflow_id="id2",
            status=WorkflowStatus.FAILED,
            agent_sequence=[],
            current_agent_index=0
        )

        stats = workflow_manager.get_workflow_statistics()

        assert stats["total_completed"] == 2
        assert stats["successful"] == 1
        assert stats["failed"] == 1


class TestBaseWorkflowManager:
    """Testes para BaseWorkflowManager"""

    @pytest.fixture
    def workflow_manager(self):
        """Instância do workflow manager base para testes"""
        return BaseWorkflowManager()

    def test_create_workflow_state(self, workflow_manager):
        """Testa criação de estado de workflow"""
        state = workflow_manager._create_workflow_state(
            "test-id",
            ["agent1", "agent2"],
            {"test": "data"}
        )

        assert state.workflow_id == "test-id"
        assert state.status == WorkflowStatus.PENDING
        assert state.agent_sequence == ["agent1", "agent2"]
        assert state.current_agent_index == 0
        assert state.accumulated_results == {"test": "data"}

    def test_update_agent_execution(self, workflow_manager):
        """Testa atualização de execução de agente"""
        state = WorkflowState(
            workflow_id="test-id",
            status=WorkflowStatus.RUNNING,
            agent_sequence=["agent1"],
            current_agent_index=0
        )

        execution = AgentExecution(
            agent_name="agent1",
            status=AgentExecutionStatus.COMPLETED,
            input_data={},
            output_data={"result": "success"},
            execution_time=1.0,
            retry_count=0
        )

        workflow_manager._update_agent_execution(state, execution)

        assert len(state.agent_executions) == 1
        assert state.agent_executions[0] == execution
        assert "result" in state.accumulated_results

    def test_advance_workflow(self, workflow_manager):
        """Testa avanço de workflow"""
        state = WorkflowState(
            workflow_id="test-id",
            status=WorkflowStatus.RUNNING,
            agent_sequence=["agent1", "agent2"],
            current_agent_index=0
        )

        workflow_manager._advance_workflow(state)

        assert state.current_agent_index == 1

    def test_check_workflow_completion_complete(self, workflow_manager):
        """Testa verificação de workflow completo"""
        state = WorkflowState(
            workflow_id="test-id",
            status=WorkflowStatus.RUNNING,
            agent_sequence=["agent1"],
            current_agent_index=1
        )

        assert workflow_manager._check_workflow_completion(state) is True

    def test_check_workflow_completion_incomplete(self, workflow_manager):
        """Testa verificação de workflow incompleto"""
        state = WorkflowState(
            workflow_id="test-id",
            status=WorkflowStatus.RUNNING,
            agent_sequence=["agent1", "agent2"],
            current_agent_index=0
        )

        assert workflow_manager._check_workflow_completion(state) is False

    def test_handle_workflow_failure(self, workflow_manager):
        """Testa tratamento de falha de workflow"""
        state = WorkflowState(
            workflow_id="test-id",
            status=WorkflowStatus.RUNNING,
            agent_sequence=[],
            current_agent_index=0
        )

        workflow_manager._handle_workflow_failure(state, "Test error")

        assert state.status == WorkflowStatus.FAILED
        assert state.error_message == "Test error"

    def test_handle_workflow_success(self, workflow_manager):
        """Testa tratamento de sucesso de workflow"""
        state = WorkflowState(
            workflow_id="test-id",
            status=WorkflowStatus.RUNNING,
            agent_sequence=[],
            current_agent_index=0
        )

        workflow_manager._handle_workflow_success(state)

        assert state.status == WorkflowStatus.COMPLETED

    def test_handle_workflow_cancellation(self, workflow_manager):
        """Testa tratamento de cancelamento de workflow"""
        state = WorkflowState(
            workflow_id="test-id",
            status=WorkflowStatus.RUNNING,
            agent_sequence=[],
            current_agent_index=0
        )

        workflow_manager._handle_workflow_cancellation(state)

        assert state.status == WorkflowStatus.CANCELLED

    def test_get_current_agent(self, workflow_manager):
        """Testa obtenção de agente atual"""
        state = WorkflowState(
            workflow_id="test-id",
            status=WorkflowStatus.RUNNING,
            agent_sequence=["agent1", "agent2"],
            current_agent_index=0
        )

        current = workflow_manager.get_current_agent(state)

        assert current == "agent1"

    def test_get_current_agent_none(self, workflow_manager):
        """Testa obtenção de agente atual quando não há"""
        state = WorkflowState(
            workflow_id="test-id",
            status=WorkflowStatus.RUNNING,
            agent_sequence=["agent1"],
            current_agent_index=1
        )

        current = workflow_manager.get_current_agent(state)

        assert current is None

    def test_get_workflow_progress(self, workflow_manager):
        """Testa cálculo de progresso de workflow"""
        state = WorkflowState(
            workflow_id="test-id",
            status=WorkflowStatus.RUNNING,
            agent_sequence=["agent1", "agent2", "agent3"],
            current_agent_index=1
        )

        progress = workflow_manager.get_workflow_progress(state)

        assert progress == 33.333333333333336

    def test_get_failed_agents(self, workflow_manager):
        """Testa obtenção de agentes que falharam"""
        state = WorkflowState(
            workflow_id="test-id",
            status=WorkflowStatus.RUNNING,
            agent_sequence=[],
            current_agent_index=0,
            agent_executions=[
                AgentExecution(
                    agent_name="agent1",
                    status=AgentExecutionStatus.COMPLETED,
                    input_data={},
                    execution_time=1.0,
                    retry_count=0
                ),
                AgentExecution(
                    agent_name="agent2",
                    status=AgentExecutionStatus.FAILED,
                    input_data={},
                    error_message="Error",
                    execution_time=1.0,
                    retry_count=0
                )
            ]
        )

        failed = workflow_manager.get_failed_agents(state)

        assert len(failed) == 1
        assert "agent2" in failed

    def test_get_completed_agents(self, workflow_manager):
        """Testa obtenção de agentes completados"""
        state = WorkflowState(
            workflow_id="test-id",
            status=WorkflowStatus.RUNNING,
            agent_sequence=[],
            current_agent_index=0,
            agent_executions=[
                AgentExecution(
                    agent_name="agent1",
                    status=AgentExecutionStatus.COMPLETED,
                    input_data={},
                    execution_time=1.0,
                    retry_count=0
                ),
                AgentExecution(
                    agent_name="agent2",
                    status=AgentExecutionStatus.FAILED,
                    input_data={},
                    error_message="Error",
                    execution_time=1.0,
                    retry_count=0
                )
            ]
        )

        completed = workflow_manager.get_completed_agents(state)

        assert len(completed) == 1
        assert "agent1" in completed

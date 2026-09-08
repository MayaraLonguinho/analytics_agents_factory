"""
Tests for Execution History
"""

import pytest
from datetime import datetime, timedelta
from ....execution_history.history import ExecutionHistory
from ....schemas import AgentExecution, AgentExecutionStatus


class TestExecutionHistory:
    """Testes para ExecutionHistory"""

    @pytest.fixture
    def history(self):
        """Instância do histórico para testes"""
        return ExecutionHistory(max_history_size=100)

    @pytest.fixture
    def sample_execution(self):
        """Execução de exemplo para testes"""
        return AgentExecution(
            agent_name="test_agent",
            status=AgentExecutionStatus.COMPLETED,
            input_data={"test": "data"},
            output_data={"result": "success"},
            execution_time=1.5,
            retry_count=0
        )

    @pytest.fixture
    def failed_execution(self):
        """Execução falha de exemplo"""
        return AgentExecution(
            agent_name="failing_agent",
            status=AgentExecutionStatus.FAILED,
            input_data={"test": "data"},
            error_message="Test error",
            execution_time=0.5,
            retry_count=2
        )

    def test_record_execution(self, history, sample_execution):
        """Testa registro de execução"""
        history.record_execution("workflow-1", sample_execution)

        workflow_history = history.get_workflow_history("workflow-1")

        assert len(workflow_history) == 1
        assert workflow_history[0] == sample_execution

    def test_record_multiple_executions(self, history, sample_execution):
        """Testa registro de múltiplas execuções"""
        history.record_execution("workflow-1", sample_execution)
        history.record_execution("workflow-1", sample_execution)
        history.record_execution("workflow-2", sample_execution)

        workflow1_history = history.get_workflow_history("workflow-1")
        workflow2_history = history.get_workflow_history("workflow-2")

        assert len(workflow1_history) == 2
        assert len(workflow2_history) == 1

    def test_get_workflow_history(self, history, sample_execution):
        """Testa obtenção de histórico de workflow"""
        history.record_execution("workflow-1", sample_execution)

        retrieved = history.get_workflow_history("workflow-1")

        assert len(retrieved) == 1
        assert retrieved[0].agent_name == "test_agent"

    def test_get_workflow_history_not_found(self, history):
        """Testa obtenção de histórico de workflow não encontrado"""
        retrieved = history.get_workflow_history("nonexistent")

        assert retrieved == []

    def test_get_agent_history(self, history, sample_execution):
        """Testa obtenção de histórico de agente"""
        history.record_execution("workflow-1", sample_execution)

        agent_history = history.get_agent_history("test_agent")

        assert len(agent_history) == 1
        assert agent_history[0].agent_name == "test_agent"

    def test_get_agent_history_with_limit(self, history, sample_execution):
        """Testa obtenção de histórico de agente com limite"""
        for i in range(10):
            history.record_execution(f"workflow-{i}", sample_execution)

        agent_history = history.get_agent_history("test_agent", limit=5)

        assert len(agent_history) == 5

    def test_get_execution_statistics(self, history, sample_execution, failed_execution):
        """Testa obtenção de estatísticas de execução"""
        history.record_execution("workflow-1", sample_execution)
        history.record_execution("workflow-1", sample_execution)
        history.record_execution("workflow-1", failed_execution)

        stats = history.get_execution_statistics("workflow-1")

        assert stats["total_executions"] == 3
        assert stats["successful"] == 2
        assert stats["failed"] == 1
        assert stats["success_rate"] == 2/3

    def test_get_execution_statistics_all(self, history, sample_execution):
        """Testa obtenção de estatísticas de todas as execuções"""
        history.record_execution("workflow-1", sample_execution)
        history.record_execution("workflow-2", sample_execution)

        stats = history.get_execution_statistics()

        assert stats["total_executions"] == 2
        assert stats["successful"] == 2

    def test_get_execution_statistics_by_agent(self, history, sample_execution, failed_execution):
        """Testa obtenção de estatísticas por agente"""
        history.record_execution("workflow-1", sample_execution)
        history.record_execution("workflow-1", failed_execution)

        stats = history.get_execution_statistics(agent_name="test_agent")

        assert stats["total_executions"] == 1
        assert stats["successful"] == 1

    def test_get_recent_executions(self, history, sample_execution):
        """Testa obtenção de execuções recentes"""
        for i in range(10):
            history.record_execution(f"workflow-{i}", sample_execution)

        recent = history.get_recent_executions(limit=5)

        assert len(recent) == 5

    def test_get_recent_executions_by_agent(self, history, sample_execution, failed_execution):
        """Testa obtenção de execuções recentes filtrado por agente"""
        history.record_execution("workflow-1", sample_execution)
        history.record_execution("workflow-2", failed_execution)

        recent = history.get_recent_executions(limit=10, agent_name="test_agent")

        assert len(recent) == 1
        assert recent[0].agent_name == "test_agent"

    def test_get_failed_executions(self, history, sample_execution, failed_execution):
        """Testa obtenção de execuções falhas"""
        history.record_execution("workflow-1", sample_execution)
        history.record_execution("workflow-2", failed_execution)

        failed = history.get_failed_executions()

        assert len(failed) == 1
        assert failed[0].agent_name == "failing_agent"

    def test_get_failed_executions_by_agent(self, history, sample_execution, failed_execution):
        """Testa obtenção de execuções falhas filtrado por agente"""
        history.record_execution("workflow-1", sample_execution)
        history.record_execution("workflow-2", failed_execution)

        failed = history.get_failed_executions(agent_name="failing_agent")

        assert len(failed) == 1
        assert failed[0].agent_name == "failing_agent"

    def test_get_executions_in_period(self, history, sample_execution):
        """Testa obtenção de execuções em período"""
        now = datetime.utcnow()
        past = now - timedelta(hours=1)

        # Criar execução com timestamp específico
        execution = AgentExecution(
            agent_name="test_agent",
            status=AgentExecutionStatus.COMPLETED,
            input_data={},
            execution_time=1.0,
            retry_count=0,
            timestamp=now
        )

        history.record_execution("workflow-1", execution)

        executions = history.get_executions_in_period(past, now + timedelta(hours=1))

        assert len(executions) == 1

    def test_clear_workflow_history(self, history, sample_execution):
        """Testa limpeza de histórico de workflow"""
        history.record_execution("workflow-1", sample_execution)
        history.record_execution("workflow-2", sample_execution)

        removed = history.clear_workflow_history("workflow-1")

        assert removed == 1
        assert history.get_workflow_history("workflow-1") == []
        assert len(history.get_workflow_history("workflow-2")) == 1

    def test_clear_old_executions(self, history, sample_execution):
        """Testa limpeza de execuções antigas"""
        # Criar execução antiga
        old_execution = AgentExecution(
            agent_name="test_agent",
            status=AgentExecutionStatus.COMPLETED,
            input_data={},
            execution_time=1.0,
            retry_count=0,
            timestamp=datetime.utcnow() - timedelta(days=40)
        )

        # Criar execução recente
        recent_execution = AgentExecution(
            agent_name="test_agent",
            status=AgentExecutionStatus.COMPLETED,
            input_data={},
            execution_time=1.0,
            retry_count=0,
            timestamp=datetime.utcnow()
        )

        history.record_execution("workflow-1", old_execution)
        history.record_execution("workflow-2", recent_execution)

        removed = history.clear_old_executions(days=30)

        assert removed == 1
        assert len(history.get_workflow_history("workflow-1")) == 0
        assert len(history.get_workflow_history("workflow-2")) == 1

    def test_get_error_summary(self, history, sample_execution, failed_execution):
        """Testa resumo de erros"""
        history.record_execution("workflow-1", sample_execution)
        history.record_execution("workflow-2", failed_execution)

        summary = history.get_error_summary()

        assert summary["total_failed"] == 1
        assert "failing_agent" in summary["agents_with_most_errors"]

    def test_max_history_size(self, history, sample_execution):
        """Testa limite máximo de histórico"""
        # Tentar adicionar mais que o limite
        for i in range(150):
            history.record_execution(f"workflow-{i}", sample_execution)

        # Verificar que não excede o limite
        assert len(history.all_executions) <= 100

"""
Tests for Orchestrator Logger
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from ....logger.orchestrator_logger import OrchestratorLogger
from ....schemas import OrchestrationInput, AgentExecution, AgentExecutionStatus


class TestOrchestratorLogger:
    """Testes para OrchestratorLogger"""

    @pytest.fixture
    def temp_dir(self):
        """Diretório temporário para testes"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def logger(self, temp_dir):
        """Instância do logger para testes"""
        return OrchestratorLogger(
            log_dir=temp_dir,
            log_level="INFO",
            enable_file_logging=True,
            enable_console_logging=False
        )

    @pytest.fixture
    def sample_input(self):
        """Input de exemplo para testes"""
        return OrchestrationInput(
            requirements="Test requirements for analytics dashboard",
            project_name="test_project",
            priority="normal"
        )

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

    def test_log_workflow_start(self, logger, sample_input):
        """Testa registro de início de workflow"""
        logger.log_workflow_start("workflow-1", sample_input)

        logs = logger.get_workflow_logs("workflow-1")

        assert len(logs) == 1
        assert logs[0]["event_type"] == "workflow_start"
        assert logs[0]["level"] == "INFO"

    def test_log_workflow_end(self, logger):
        """Testa registro de fim de workflow"""
        output_data = {
            "workflow_id": "workflow-1",
            "status": "completed",
            "execution_time": 120.0,
            "agent_executions": []
        }

        logger.log_workflow_end("workflow-1", output_data)

        logs = logger.get_workflow_logs("workflow-1")

        assert len(logs) == 1
        assert logs[0]["event_type"] == "workflow_end"
        assert logs[0]["level"] == "INFO"

    def test_log_agent_start(self, logger):
        """Testa registro de início de agente"""
        logger.log_agent_start("workflow-1", "test_agent", {"test": "data"})

        logs = logger.get_workflow_logs("workflow-1")

        assert len(logs) == 1
        assert logs[0]["event_type"] == "agent_start"
        assert logs[0]["agent_name"] == "test_agent"

    def test_log_agent_end_success(self, logger, sample_execution):
        """Testa registro de fim de agente com sucesso"""
        logger.log_agent_end("workflow-1", "test_agent", sample_execution)

        logs = logger.get_workflow_logs("workflow-1")

        assert len(logs) == 1
        assert logs[0]["event_type"] == "agent_end"
        assert logs[0]["level"] == "INFO"
        assert logs[0]["agent_name"] == "test_agent"

    def test_log_agent_end_failure(self, logger):
        """Testa registro de fim de agente com falha"""
        failed_execution = AgentExecution(
            agent_name="test_agent",
            status=AgentExecutionStatus.FAILED,
            input_data={},
            error_message="Test error",
            execution_time=0.5,
            retry_count=1
        )

        logger.log_agent_end("workflow-1", "test_agent", failed_execution)

        logs = logger.get_workflow_logs("workflow-1")

        assert len(logs) == 1
        assert logs[0]["event_type"] == "agent_end"
        assert logs[0]["level"] == "ERROR"

    def test_log_error(self, logger):
        """Testa registro de erro"""
        error = Exception("Test error message")
        logger.log_error("workflow-1", "test_agent", error, {"context": "test"})

        logs = logger.get_workflow_logs("workflow-1")

        assert len(logs) == 1
        assert logs[0]["event_type"] == "error"
        assert logs[0]["level"] == "ERROR"
        assert "Test error message" in logs[0]["message"]

    def test_get_workflow_logs(self, logger, sample_input):
        """Testa obtenção de logs de workflow"""
        logger.log_workflow_start("workflow-1", sample_input)
        logger.log_agent_start("workflow-1", "agent1", {})

        logs = logger.get_workflow_logs("workflow-1")

        assert len(logs) == 2

    def test_get_workflow_logs_not_found(self, logger):
        """Testa obtenção de logs de workflow não encontrado"""
        logs = logger.get_workflow_logs("nonexistent")

        assert logs == []

    def test_get_logs_by_level(self, logger):
        """Testa obtenção de logs filtrado por nível"""
        logger.log_workflow_start("workflow-1", {"requirements": "test", "project_name": "test"})

        error = Exception("Test error")
        logger.log_error("workflow-1", "agent1", error)

        info_logs = logger.get_logs_by_level("workflow-1", "INFO")
        error_logs = logger.get_logs_by_level("workflow-1", "ERROR")

        assert len(info_logs) == 1
        assert len(error_logs) == 1

    def test_get_logs_by_event_type(self, logger, sample_input):
        """Testa obtenção de logs filtrado por tipo de evento"""
        logger.log_workflow_start("workflow-1", sample_input)
        logger.log_agent_start("workflow-1", "agent1", {})

        start_logs = logger.get_logs_by_event_type("workflow-1", "workflow_start")
        agent_logs = logger.get_logs_by_event_type("workflow-1", "agent_start")

        assert len(start_logs) == 1
        assert len(agent_logs) == 1

    def test_get_logs_by_agent(self, logger):
        """Testa obtenção de logs filtrado por agente"""
        logger.log_agent_start("workflow-1", "agent1", {})
        logger.log_agent_start("workflow-1", "agent2", {})

        agent1_logs = logger.get_logs_by_agent("workflow-1", "agent1")
        agent2_logs = logger.get_logs_by_agent("workflow-1", "agent2")

        assert len(agent1_logs) == 1
        assert len(agent2_logs) == 1

    def test_get_audit_records(self, logger, sample_input):
        """Testa obtenção de registros de auditoria"""
        logger.log_workflow_start("workflow-1", sample_input)

        audit_records = logger.get_audit_records(workflow_id="workflow-1")

        assert len(audit_records) == 1
        assert audit_records[0]["action"] == "workflow_start"

    def test_get_audit_records_by_action(self, logger, sample_input):
        """Testa obtenção de registros de auditoria filtrado por ação"""
        logger.log_workflow_start("workflow-1", sample_input)

        start_records = logger.get_audit_records(action="workflow_start")

        assert len(start_records) == 1

    def test_get_audit_records_with_limit(self, logger, sample_input):
        """Testa obtenção de registros de auditoria com limite"""
        for i in range(10):
            logger.log_workflow_start(f"workflow-{i}", sample_input)

        audit_records = logger.get_audit_records(limit=5)

        assert len(audit_records) == 5

    def test_clear_workflow_logs(self, logger, sample_input):
        """Testa limpeza de logs de workflow"""
        logger.log_workflow_start("workflow-1", sample_input)
        logger.clear_workflow_logs("workflow-1")

        logs = logger.get_workflow_logs("workflow-1")

        assert logs == []

    def test_clear_old_logs(self, logger):
        """Testa limpeza de logs antigos"""
        from datetime import datetime, timedelta

        # Criar logs antigos manualmente
        old_log = logger._create_execution_log(
            "workflow-1",
            "INFO",
            "test_event",
            "Test message"
        )
        old_log.timestamp = datetime.utcnow() - timedelta(days=35)
        logger.logs["workflow-1"] = [old_log]

        # Criar logs recentes
        logger.log_workflow_start("workflow-2", {"requirements": "test", "project_name": "test"})

        removed = logger.clear_old_logs(days=30)

        assert removed >= 1

    def test_get_log_statistics(self, logger, sample_input):
        """Testa obtenção de estatísticas de logs"""
        logger.log_workflow_start("workflow-1", sample_input)
        logger.log_agent_start("workflow-1", "agent1", {})

        stats = logger.get_log_statistics()

        assert stats["total_logs"] == 2
        assert stats["total_workflows"] == 1
        assert "logs_by_level" in stats
        assert "logs_by_event_type" in stats

    def test_multiple_workflows(self, logger, sample_input):
        """Testa logs de múltiplos workflows"""
        logger.log_workflow_start("workflow-1", sample_input)
        logger.log_workflow_start("workflow-2", sample_input)

        workflow1_logs = logger.get_workflow_logs("workflow-1")
        workflow2_logs = logger.get_workflow_logs("workflow-2")

        assert len(workflow1_logs) == 1
        assert len(workflow2_logs) == 1

    def test_log_file_creation(self, logger, sample_input, temp_dir):
        """Testa criação de arquivo de log"""
        logger.log_workflow_start("workflow-1", sample_input)

        log_file = Path(temp_dir) / "workflow-1.jsonl"
        assert log_file.exists()

    def test_audit_file_creation(self, logger, sample_input, temp_dir):
        """Testa criação de arquivo de auditoria"""
        logger.log_workflow_start("workflow-1", sample_input)

        audit_file = Path(temp_dir) / "audit.jsonl"
        assert audit_file.exists()

    def test_log_file_disabled(self, temp_dir):
        """Testa logging de arquivo desabilitado"""
        logger = OrchestratorLogger(
            log_dir=temp_dir,
            enable_file_logging=False,
            enable_console_logging=False
        )

        logger.log_workflow_start("workflow-1", {"requirements": "test", "project_name": "test"})

        log_file = Path(temp_dir) / "workflow-1.jsonl"
        assert not log_file.exists()

    def test_error_with_context(self, logger):
        """Testa registro de erro com contexto"""
        error = ValueError("Invalid value")
        context = {"field": "test_field", "value": "invalid"}

        logger.log_error("workflow-1", "agent1", error, context)

        logs = logger.get_workflow_logs("workflow-1")

        assert len(logs) == 1
        assert logs[0]["data"]["context"] == context

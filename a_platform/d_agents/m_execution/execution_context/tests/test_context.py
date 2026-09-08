"""
Tests for Execution Context
"""

import pytest
from datetime import datetime
from ....execution_context.context import ExecutionContext
from ....schemas import OrchestrationInput


class TestExecutionContext:
    """Testes para ExecutionContext"""

    @pytest.fixture
    def context(self):
        """Instância do contexto para testes"""
        return ExecutionContext()

    @pytest.fixture
    def sample_input(self):
        """Input de exemplo para testes"""
        return OrchestrationInput(
            requirements="Test requirements",
            project_name="test_project"
        )

    def test_create_context(self, context, sample_input):
        """Testa criação de contexto"""
        context.create_context("test-id", sample_input)

        retrieved = context.get_context("test-id")

        assert retrieved is not None
        assert retrieved["workflow_id"] == "test-id"
        assert "input_data" in retrieved
        assert "results" in retrieved
        assert "metadata" in retrieved

    def test_create_context_with_dict(self, context):
        """Testa criação de contexto com dicionário"""
        input_data = {"test": "data"}
        context.create_context("test-id", input_data)

        retrieved = context.get_context("test-id")

        assert retrieved is not None
        assert retrieved["input_data"] == input_data

    def test_get_context_not_found(self, context):
        """Testa obtenção de contexto não encontrado"""
        with pytest.raises(ValueError, match="not found"):
            context.get_context("nonexistent")

    def test_update_context(self, context, sample_input):
        """Testa atualização de contexto"""
        context.create_context("test-id", sample_input)
        context.update_context("test-id", "test_key", "test_value")

        retrieved = context.get_context("test-id")

        assert retrieved["test_key"] == "test_value"

    def test_merge_results(self, context, sample_input):
        """Testa mesclagem de resultados"""
        context.create_context("test-id", sample_input)
        context.merge_results("test-id", "agent1", {"result1": "value1"})
        context.merge_results("test-id", "agent2", {"result2": "value2"})

        retrieved = context.get_context("test-id")

        assert "result1" in retrieved["results"]
        assert "result2" in retrieved["results"]
        assert retrieved["results"]["result1"] == "value1"
        assert retrieved["results"]["result2"] == "value2"

    def test_merge_results_nested(self, context, sample_input):
        """Testa mesclagem de resultados aninhados"""
        context.create_context("test-id", sample_input)
        context.merge_results("test-id", "agent1", {"data": {"nested": "value1"}})
        context.merge_results("test-id", "agent2", {"data": {"nested2": "value2"}})

        retrieved = context.get_context("test-id")

        assert retrieved["results"]["data"]["nested"] == "value1"
        assert retrieved["results"]["data"]["nested2"] == "value2"

    def test_merge_results_lists(self, context, sample_input):
        """Testa mesclagem de resultados com listas"""
        context.create_context("test-id", sample_input)
        context.merge_results("test-id", "agent1", {"items": [1, 2]})
        context.merge_results("test-id", "agent2", {"items": [3, 4]})

        retrieved = context.get_context("test-id")

        assert retrieved["results"]["items"] == [1, 2, 3, 4]

    def test_delete_context(self, context, sample_input):
        """Testa deleção de contexto"""
        context.create_context("test-id", sample_input)
        context.delete_context("test-id")

        with pytest.raises(ValueError, match="not found"):
            context.get_context("test-id")

    def test_create_snapshot(self, context, sample_input):
        """Testa criação de snapshot"""
        context.create_context("test-id", sample_input)
        context.merge_results("test-id", "agent1", {"result": "value"})

        snapshot = context.create_snapshot("test-id", "agent1")

        assert snapshot.workflow_id == "test-id"
        assert snapshot.agent_name == "agent1"
        assert snapshot.context_data is not None
        assert "result" in snapshot.context_data["results"]

    def test_get_snapshots(self, context, sample_input):
        """Testa obtenção de snapshots"""
        context.create_context("test-id", sample_input)
        context.create_snapshot("test-id", "agent1")
        context.create_snapshot("test-id", "agent2")

        snapshots = context.get_snapshots("test-id")

        assert len(snapshots) == 2

    def test_get_snapshots_by_agent(self, context, sample_input):
        """Testa obtenção de snapshots filtrado por agente"""
        context.create_context("test-id", sample_input)
        context.create_snapshot("test-id", "agent1")
        context.create_snapshot("test-id", "agent2")

        agent1_snapshots = context.get_snapshots("test-id", "agent1")

        assert len(agent1_snapshots) == 1
        assert agent1_snapshots[0].agent_name == "agent1"

    def test_restore_snapshot(self, context, sample_input):
        """Testa restauração de snapshot"""
        context.create_context("test-id", sample_input)
        context.merge_results("test-id", "agent1", {"result": "value1"})

        snapshot = context.create_snapshot("test-id", "agent1")

        # Modificar contexto
        context.merge_results("test-id", "agent2", {"result": "value2"})

        # Restaurar snapshot
        context.restore_snapshot("test-id", snapshot.snapshot_id)

        retrieved = context.get_context("test-id")

        assert "value1" in retrieved["results"].get("result", "")
        assert "value2" not in str(retrieved["results"])

    def test_restore_snapshot_not_found(self, context, sample_input):
        """Testa restauração de snapshot não encontrado"""
        context.create_context("test-id", sample_input)

        with pytest.raises(ValueError, match="not found"):
            context.restore_snapshot("test-id", "nonexistent-id")

    def test_get_agent_results(self, context, sample_input):
        """Testa obtenção de resultados de agente específico"""
        context.create_context("test-id", sample_input)
        context.merge_results("test-id", "agent1", {"result": "value1"})
        context.merge_results("test-id", "agent2", {"result": "value2"})

        agent1_results = context.get_agent_results("test-id", "agent1")

        assert agent1_results is not None
        assert agent1_results["result"] == "value1"

    def test_get_agent_results_not_found(self, context, sample_input):
        """Testa obtenção de resultados de agente não encontrado"""
        context.create_context("test-id", sample_input)

        results = context.get_agent_results("test-id", "nonexistent")

        assert results is None

    def test_get_all_results(self, context, sample_input):
        """Testa obtenção de todos os resultados"""
        context.create_context("test-id", sample_input)
        context.merge_results("test-id", "agent1", {"result1": "value1"})
        context.merge_results("test-id", "agent2", {"result2": "value2"})

        all_results = context.get_all_results("test-id")

        assert "result1" in all_results
        assert "result2" in all_results

    def test_add_metadata(self, context, sample_input):
        """Testa adição de metadados"""
        context.create_context("test-id", sample_input)
        context.add_metadata("test-id", "meta_key", "meta_value")

        metadata = context.get_metadata("test-id")

        assert metadata["meta_key"] == "meta_value"

    def test_get_metadata_specific_key(self, context, sample_input):
        """Testa obtenção de metadado específico"""
        context.create_context("test-id", sample_input)
        context.add_metadata("test-id", "meta_key", "meta_value")

        value = context.get_metadata("test-id", "meta_key")

        assert value == "meta_value"

    def test_get_metadata_all(self, context, sample_input):
        """Testa obtenção de todos os metadados"""
        context.create_context("test-id", sample_input)
        context.add_metadata("test-id", "key1", "value1")
        context.add_metadata("test-id", "key2", "value2")

        metadata = context.get_metadata("test-id")

        assert metadata["key1"] == "value1"
        assert metadata["key2"] == "value2"

    def test_list_active_contexts(self, context, sample_input):
        """Testa listagem de contextos ativos"""
        context.create_context("id1", sample_input)
        context.create_context("id2", sample_input)

        active = context.list_active_contexts()

        assert len(active) == 2
        assert "id1" in active
        assert "id2" in active

    def test_clear_old_contexts(self, context, sample_input):
        """Testa limpeza de contextos antigos"""
        # Criar contexto antigo manualmente
        context.create_context("old-id", sample_input)
        # Modificar timestamp para ser antigo
        old_timestamp = datetime.fromisoformat(
            context.contexts["old-id"]["metadata"]["updated_at"]
        ).replace(year=2020)

        context.contexts["old-id"]["metadata"]["updated_at"] = old_timestamp.isoformat()

        # Criar contexto recente
        context.create_context("new-id", sample_input)

        # Limpar contextos antigos (mais de 1 hora)
        removed = context.clear_old_contexts(max_age_hours=1)

        assert removed == 1
        assert "old-id" not in context.contexts
        assert "new-id" in context.contexts

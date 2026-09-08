"""
Tests for File State Manager
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from ....state_manager.file_state import FileStateManager
from ....state_manager.base_state import BaseStateManager


class TestFileStateManager:
    """Testes para FileStateManager"""

    @pytest.fixture
    def temp_dir(self):
        """Diretório temporário para testes"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def state_manager(self, temp_dir):
        """Instância do state manager para testes"""
        return FileStateManager(state_dir=temp_dir)

    @pytest.fixture
    def sample_state(self):
        """Estado de exemplo para testes"""
        return {
            "workflow_id": "test-workflow",
            "status": "running",
            "agent_sequence": ["agent1", "agent2"],
            "current_agent_index": 0,
            "accumulated_results": {"test": "data"}
        }

    def test_save_state(self, state_manager, sample_state):
        """Testa salvamento de estado"""
        state_manager.save_state("test-id", sample_state)

        retrieved = state_manager.load_state("test-id")

        assert retrieved is not None
        assert retrieved["workflow_id"] == "test-workflow"
        assert retrieved["status"] == "running"

    def test_load_state(self, state_manager, sample_state):
        """Testa carregamento de estado"""
        state_manager.save_state("test-id", sample_state)

        retrieved = state_manager.load_state("test-id")

        assert retrieved == sample_state

    def test_load_state_not_found(self, state_manager):
        """Testa carregamento de estado não encontrado"""
        retrieved = state_manager.load_state("nonexistent")

        assert retrieved is None

    def test_delete_state(self, state_manager, sample_state):
        """Testa deleção de estado"""
        state_manager.save_state("test-id", sample_state)
        state_manager.delete_state("test-id")

        retrieved = state_manager.load_state("test-id")

        assert retrieved is None

    def test_list_saved_states(self, state_manager, sample_state):
        """Testa listagem de estados salvos"""
        state_manager.save_state("id1", sample_state)
        state_manager.save_state("id2", sample_state)

        saved = state_manager.list_saved_states()

        assert len(saved) == 2
        assert "id1" in saved
        assert "id2" in saved

    def test_get_state_size(self, state_manager, sample_state):
        """Testa obtenção de tamanho de estado"""
        state_manager.save_state("test-id", sample_state)

        size = state_manager.get_state_size("test-id")

        assert size is not None
        assert size > 0

    def test_get_state_size_not_found(self, state_manager):
        """Testa obtenção de tamanho de estado não encontrado"""
        size = state_manager.get_state_size("nonexistent")

        assert size is None

    def test_cleanup_old_states(self, state_manager, sample_state):
        """Testa limpeza de estados antigos"""
        from datetime import datetime, timedelta

        # Salvar estado
        state_manager.save_state("test-id", sample_state)

        # Modificar arquivo para ser antigo
        state_file = state_manager._get_state_file_path("test-id")
        old_time = datetime.now() - timedelta(hours=25)
        import os
        import time
        old_timestamp = old_time.timestamp()
        os.utime(state_file, (old_timestamp, old_timestamp))

        # Limpar estados antigos
        removed = state_manager.cleanup_old_states(max_age_hours=24)

        assert removed == 1
        assert state_manager.load_state("test-id") is None

    def test_get_total_storage_size(self, state_manager, sample_state):
        """Testa obtenção de tamanho total de armazenamento"""
        state_manager.save_state("id1", sample_state)
        state_manager.save_state("id2", sample_state)

        total_size = state_manager.get_total_storage_size()

        assert total_size > 0

    def test_export_state(self, state_manager, sample_state, temp_dir):
        """Testa exportação de estado"""
        state_manager.save_state("test-id", sample_state)

        export_path = Path(temp_dir) / "exported_state.json"
        state_manager.export_state("test-id", str(export_path))

        assert export_path.exists()

        # Verificar conteúdo
        import json
        with open(export_path) as f:
            exported = json.load(f)

        assert exported["workflow_id"] == "test-workflow"

    def test_export_state_not_found(self, state_manager, temp_dir):
        """Testa exportação de estado não encontrado"""
        export_path = Path(temp_dir) / "exported_state.json"

        with pytest.raises(ValueError, match="No state found"):
            state_manager.export_state("nonexistent", str(export_path))

    def test_import_state(self, state_manager, temp_dir):
        """Testa importação de estado"""
        # Criar arquivo para importar
        import json
        import_file = Path(temp_dir) / "import_state.json"
        import_data = {
            "workflow_id": "imported-workflow",
            "status": "completed",
            "agent_sequence": ["agent1"]
        }

        with open(import_file, 'w') as f:
            json.dump(import_data, f)

        state_manager.import_state(str(import_file), "new-id")

        retrieved = state_manager.load_state("new-id")

        assert retrieved is not None
        assert retrieved["workflow_id"] == "new-id"
        assert retrieved["status"] == "completed"

    def test_import_state_file_not_found(self, state_manager, temp_dir):
        """Testa importação de arquivo não encontrado"""
        import_file = Path(temp_dir) / "nonexistent.json"

        with pytest.raises(FileNotFoundError):
            state_manager.import_state(str(import_file), "new-id")

    def test_validate_state_valid(self, state_manager, sample_state):
        """Testa validação de estado válido"""
        state_manager.save_state("test-id", sample_state)

        is_valid = state_manager.validate_state("test-id")

        assert is_valid is True

    def test_validate_state_invalid(self, state_manager):
        """Testa validação de estado inválido"""
        invalid_state = {"incomplete": "state"}
        state_manager.save_state("test-id", invalid_state)

        is_valid = state_manager.validate_state("test-id")

        assert is_valid is False

    def test_validate_state_not_found(self, state_manager):
        """Testa validação de estado não encontrado"""
        is_valid = state_manager.validate_state("nonexistent")

        assert is_valid is False

    def test_get_state_metadata(self, state_manager, sample_state):
        """Testa obtenção de metadados de estado"""
        state_manager.save_state("test-id", sample_state)

        metadata = state_manager.get_state_metadata("test-id")

        assert metadata is not None
        assert metadata["workflow_id"] == "test-id"
        assert "size_bytes" in metadata
        assert "created_at" in metadata
        assert "modified_at" in metadata

    def test_get_state_metadata_not_found(self, state_manager):
        """Testa obtenção de metadados de estado não encontrado"""
        metadata = state_manager.get_state_metadata("nonexistent")

        assert metadata is None

    def test_cache_state(self, state_manager, sample_state):
        """Testa cache de estado"""
        state_manager.save_state("test-id", sample_state)

        # Verificar que está no cache
        cached = state_manager._get_cached_state("test-id")

        assert cached is not None
        assert cached == sample_state

    def test_clear_cache(self, state_manager, sample_state):
        """Testa limpeza de cache"""
        state_manager.save_state("test-id", sample_state)
        state_manager._clear_cache("test-id")

        cached = state_manager._get_cached_state("test-id")

        assert cached is None

    def test_clear_all_cache(self, state_manager, sample_state):
        """Testa limpeza de todo o cache"""
        state_manager.save_state("id1", sample_state)
        state_manager.save_state("id2", sample_state)

        state_manager.clear_all_cache()

        assert len(state_manager.get_cached_workflows()) == 0

    def test_get_cached_workflows(self, state_manager, sample_state):
        """Testa obtenção de workflows cacheados"""
        state_manager.save_state("id1", sample_state)
        state_manager.save_state("id2", sample_state)

        cached = state_manager.get_cached_workflows()

        assert len(cached) == 2
        assert "id1" in cached
        assert "id2" in cached


class TestBaseStateManager:
    """Testes para BaseStateManager"""

    @pytest.fixture
    def state_manager(self):
        """Instância do state manager base para testes"""
        return BaseStateManager()

    def test_cache_state(self, state_manager):
        """Testa cache de estado"""
        sample_state = {"test": "data"}
        state_manager._cache_state("test-id", sample_state)

        cached = state_manager._get_cached_state("test-id")

        assert cached == sample_state

    def test_get_cached_state(self, state_manager):
        """Testa obtenção de estado cacheado"""
        sample_state = {"test": "data"}
        state_manager._cache_state("test-id", sample_state)

        cached = state_manager._get_cached_state("test-id")

        assert cached is not None
        assert cached == sample_state

    def test_get_cached_state_not_found(self, state_manager):
        """Testa obtenção de estado cacheado não encontrado"""
        cached = state_manager._get_cached_state("nonexistent")

        assert cached is None

    def test_clear_cache(self, state_manager):
        """Testa limpeza de cache"""
        state_manager._cache_state("test-id", {"test": "data"})
        state_manager._clear_cache("test-id")

        cached = state_manager._get_cached_state("test-id")

        assert cached is None

    def test_clear_all_cache(self, state_manager):
        """Testa limpeza de todo o cache"""
        state_manager._cache_state("id1", {"test": "data1"})
        state_manager._cache_state("id2", {"test": "data2"})

        state_manager.clear_all_cache()

        assert len(state_manager.get_cached_workflows()) == 0

    def test_get_cached_workflows(self, state_manager):
        """Testa obtenção de workflows cacheados"""
        state_manager._cache_state("id1", {"test": "data1"})
        state_manager._cache_state("id2", {"test": "data2"})

        cached = state_manager.get_cached_workflows()

        assert len(cached) == 2
        assert "id1" in cached
        assert "id2" in cached

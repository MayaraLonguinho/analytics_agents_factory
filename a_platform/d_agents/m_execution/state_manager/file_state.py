"""
File State Manager - Implementação com persistência em arquivo
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from threading import Lock
from datetime import datetime
from .base_state import BaseStateManager


class FileStateManager(BaseStateManager):
    """
    Implementação do gestor de estado com persistência em arquivo.
    Salva estados em arquivos JSON no diretório especificado.
    """

    def __init__(self, state_dir: str = ".orchestrator_state"):
        """
        Inicializa o FileStateManager.

        Args:
            state_dir: Diretório para salvar estados
        """
        super().__init__()
        self.state_dir = Path(state_dir)
        self.lock = Lock()

        # Criar diretório se não existir
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def _get_state_file_path(self, workflow_id: str) -> Path:
        """
        Retorna caminho do arquivo de estado para um workflow.

        Args:
            workflow_id: ID do workflow

        Returns:
            Path do arquivo de estado
        """
        # Sanitizar workflow_id para uso em nome de arquivo
        safe_id = workflow_id.replace('/', '_').replace('\\', '_')
        return self.state_dir / f"{safe_id}.json"

    def save_state(self, workflow_id: str, state: Dict[str, Any]) -> None:
        """
        Salva o estado de um workflow em arquivo.

        Args:
            workflow_id: Identificador do workflow
            state: Estado a salvar
        """
        with self.lock:
            # Cacheiar estado
            self._cache_state(workflow_id, state)

            # Salvar em arquivo
            state_file = self._get_state_file_path(workflow_id)

            try:
                with open(state_file, 'w') as f:
                    json.dump(state, f, indent=2, default=str)
            except Exception as e:
                raise IOError(f"Failed to save state for workflow {workflow_id}: {e}")

    def load_state(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Carrega o estado de um workflow do arquivo.

        Args:
            workflow_id: Identificador do workflow

        Returns:
            Estado salvo ou None se não encontrado
        """
        with self.lock:
            # Tentar cache primeiro
            cached = self._get_cached_state(workflow_id)
            if cached:
                return cached

            # Carregar do arquivo
            state_file = self._get_state_file_path(workflow_id)

            if not state_file.exists():
                return None

            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)

                # Cacheiar estado carregado
                self._cache_state(workflow_id, state)

                return state

            except Exception as e:
                raise IOError(f"Failed to load state for workflow {workflow_id}: {e}")

    def delete_state(self, workflow_id: str) -> None:
        """
        Remove o estado de um workflow.

        Args:
            workflow_id: Identificador do workflow
        """
        with self.lock:
            # Limpar cache
            self._clear_cache(workflow_id)

            # Remover arquivo
            state_file = self._get_state_file_path(workflow_id)

            if state_file.exists():
                try:
                    state_file.unlink()
                except Exception as e:
                    raise IOError(f"Failed to delete state for workflow {workflow_id}: {e}")

    def list_saved_states(self) -> list:
        """
        Lista todos os workflows com estado salvo.

        Returns:
            Lista de IDs de workflows com estado salvo
        """
        with self.lock:
            if not self.state_dir.exists():
                return []

            state_files = self.state_dir.glob("*.json")
            workflow_ids = []

            for state_file in state_files:
                # Extrair workflow_id do nome do arquivo
                workflow_id = state_file.stem.replace('_', '/')
                workflow_ids.append(workflow_id)

            return workflow_ids

    def get_state_size(self, workflow_id: str) -> Optional[int]:
        """
        Retorna o tamanho do estado de um workflow em bytes.

        Args:
            workflow_id: ID do workflow

        Returns:
            Tamanho em bytes ou None se não encontrado
        """
        state_file = self._get_state_file_path(workflow_id)

        if not state_file.exists():
            return None

        return state_file.stat().st_size

    def cleanup_old_states(self, max_age_hours: int = 24) -> int:
        """
        Limpa estados antigos.

        Args:
            max_age_hours: Idade máxima em horas

        Returns:
            Número de estados removidos
        """
        from datetime import datetime, timedelta

        with self.lock:
            cutoff = datetime.now() - timedelta(hours=max_age_hours)
            removed = 0

            for state_file in self.state_dir.glob("*.json"):
                file_mtime = datetime.fromtimestamp(state_file.stat().st_mtime)

                if file_mtime < cutoff:
                    try:
                        state_file.unlink()
                        # Limpar cache correspondente
                        workflow_id = state_file.stem.replace('_', '/')
                        self._clear_cache(workflow_id)
                        removed += 1
                    except Exception:
                        pass

            return removed

    def get_total_storage_size(self) -> int:
        """
        Retorna o tamanho total de armazenamento usado.

        Returns:
            Tamanho total em bytes
        """
        if not self.state_dir.exists():
            return 0

        total_size = 0
        for state_file in self.state_dir.glob("*.json"):
            total_size += state_file.stat().st_size

        return total_size

    def export_state(self, workflow_id: str, export_path: str) -> None:
        """
        Exporta estado de um workflow para um arquivo específico.

        Args:
            workflow_id: ID do workflow
            export_path: Caminho para exportar
        """
        state = self.load_state(workflow_id)

        if not state:
            raise ValueError(f"No state found for workflow {workflow_id}")

        export_file = Path(export_path)
        export_file.parent.mkdir(parents=True, exist_ok=True)

        with open(export_file, 'w') as f:
            json.dump(state, f, indent=2, default=str)

    def import_state(self, import_path: str, workflow_id: str) -> None:
        """
        Importa estado de um arquivo para um workflow.

        Args:
            import_path: Caminho do arquivo a importar
            workflow_id: ID do workflow
        """
        import_file = Path(import_path)

        if not import_file.exists():
            raise FileNotFoundError(f"Import file not found: {import_path}")

        with open(import_file, 'r') as f:
            state = json.load(f)

        # Atualizar workflow_id no estado
        if isinstance(state, dict):
            state['workflow_id'] = workflow_id

        self.save_state(workflow_id, state)

    def validate_state(self, workflow_id: str) -> bool:
        """
        Valida se o estado de um workflow é válido.

        Args:
            workflow_id: ID do workflow

        Returns:
            True se válido, False caso contrário
        """
        try:
            state = self.load_state(workflow_id)

            if not state:
                return False

            # Verificar campos obrigatórios
            required_fields = ['workflow_id', 'status', 'agent_sequence']

            for field in required_fields:
                if field not in state:
                    return False

            return True

        except Exception:
            return False

    def get_state_metadata(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Retorna metadados do estado de um workflow.

        Args:
            workflow_id: ID do workflow

        Returns:
            Dicionário com metadados ou None
        """
        state_file = self._get_state_file_path(workflow_id)

        if not state_file.exists():
            return None

        stat = state_file.stat()

        return {
            "workflow_id": workflow_id,
            "file_path": str(state_file),
            "size_bytes": stat.st_size,
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "is_cached": workflow_id in self.cache
        }

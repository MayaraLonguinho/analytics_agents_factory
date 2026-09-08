"""
Execution Context - Contexto de execução compartilhado
"""

from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from threading import Lock
from ...interfaces import IExecutionContext
from ...schemas import ContextSnapshot


class ExecutionContext(IExecutionContext):
    """
    Implementação do contexto de execução.
    Responsável por manter contexto compartilhado entre agentes.
    """

    def __init__(self):
        """
        Inicializa o contexto de execução.
        """
        self.contexts: Dict[str, Dict[str, Any]] = {}
        self.snapshots: Dict[str, List[ContextSnapshot]] = {}
        self.lock = Lock()

    def create_context(
        self,
        workflow_id: str,
        input_data: Union[Dict[str, Any], object]
    ) -> None:
        """
        Cria um novo contexto de execução.

        Args:
            workflow_id: ID do workflow
            input_data: Dados de entrada
        """
        with self.lock:
            self.contexts[workflow_id] = {
                "workflow_id": workflow_id,
                "input_data": input_data.dict() if hasattr(input_data, 'dict') else input_data,
                "results": {},
                "metadata": {
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
            }
            self.snapshots[workflow_id] = []

    def get_context(self, workflow_id: str) -> Dict[str, Any]:
        """
        Recupera contexto de execução.

        Args:
            workflow_id: ID do workflow

        Returns:
            Dicionário com contexto
        """
        with self.lock:
            if workflow_id not in self.contexts:
                raise ValueError(f"Context for workflow {workflow_id} not found")

            return self.contexts[workflow_id].copy()

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
        with self.lock:
            if workflow_id not in self.contexts:
                raise ValueError(f"Context for workflow {workflow_id} not found")

            self.contexts[workflow_id][key] = value
            self.contexts[workflow_id]["metadata"]["updated_at"] = datetime.utcnow().isoformat()

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
        with self.lock:
            if workflow_id not in self.contexts:
                raise ValueError(f"Context for workflow {workflow_id} not found")

            # Mesclar resultados recursivamente
            def merge_dict(base: Dict, new: Dict) -> Dict:
                merged = base.copy()
                for key, value in new.items():
                    if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                        merged[key] = merge_dict(merged[key], value)
                    elif key in merged and isinstance(merged[key], list) and isinstance(value, list):
                        merged[key] = merged[key] + value
                    else:
                        merged[key] = value
                return merged

            self.contexts[workflow_id]["results"] = merge_dict(
                self.contexts[workflow_id].get("results", {}),
                results
            )

            # Adicionar timestamp do agente
            if "agent_timestamps" not in self.contexts[workflow_id]:
                self.contexts[workflow_id]["agent_timestamps"] = {}

            self.contexts[workflow_id]["agent_timestamps"][agent_name] = datetime.utcnow().isoformat()
            self.contexts[workflow_id]["metadata"]["updated_at"] = datetime.utcnow().isoformat()

    def delete_context(self, workflow_id: str) -> None:
        """
        Remove contexto de execução.

        Args:
            workflow_id: ID do workflow
        """
        with self.lock:
            if workflow_id in self.contexts:
                del self.contexts[workflow_id]

            if workflow_id in self.snapshots:
                del self.snapshots[workflow_id]

    def create_snapshot(
        self,
        workflow_id: str,
        agent_name: Optional[str] = None
    ) -> ContextSnapshot:
        """
        Cria um snapshot do contexto atual.

        Args:
            workflow_id: ID do workflow
            agent_name: Nome do agente que criou o snapshot (opcional)

        Returns:
            ContextSnapshot criado
        """
        with self.lock:
            if workflow_id not in self.contexts:
                raise ValueError(f"Context for workflow {workflow_id} not found")

            import uuid
            snapshot = ContextSnapshot(
                workflow_id=workflow_id,
                snapshot_id=str(uuid.uuid4()),
                timestamp=datetime.utcnow(),
                context_data=self.contexts[workflow_id].copy(),
                agent_name=agent_name
            )

            self.snapshots[workflow_id].append(snapshot)
            return snapshot

    def get_snapshots(
        self,
        workflow_id: str,
        agent_name: Optional[str] = None
    ) -> List[ContextSnapshot]:
        """
        Recupera snapshots de um workflow.

        Args:
            workflow_id: ID do workflow
            agent_name: Filtrar por agente (opcional)

        Returns:
            Lista de snapshots
        """
        with self.lock:
            if workflow_id not in self.snapshots:
                return []

            snapshots = self.snapshots[workflow_id]

            if agent_name:
                snapshots = [s for s in snapshots if s.agent_name == agent_name]

            return snapshots

    def restore_snapshot(
        self,
        workflow_id: str,
        snapshot_id: str
    ) -> None:
        """
        Restaura contexto de um snapshot.

        Args:
            workflow_id: ID do workflow
            snapshot_id: ID do snapshot
        """
        with self.lock:
            if workflow_id not in self.snapshots:
                raise ValueError(f"No snapshots for workflow {workflow_id}")

            snapshot = next(
                (s for s in self.snapshots[workflow_id] if s.snapshot_id == snapshot_id),
                None
            )

            if not snapshot:
                raise ValueError(f"Snapshot {snapshot_id} not found")

            self.contexts[workflow_id] = snapshot.context_data.copy()
            self.contexts[workflow_id]["metadata"]["updated_at"] = datetime.utcnow().isoformat()

    def get_agent_results(
        self,
        workflow_id: str,
        agent_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Recupera resultados específicos de um agente.

        Args:
            workflow_id: ID do workflow
            agent_name: Nome do agente

        Returns:
            Resultados do agente ou None
        """
        with self.lock:
            if workflow_id not in self.contexts:
                return None

            results = self.contexts[workflow_id].get("results", {})
            return results.get(agent_name)

    def get_all_results(self, workflow_id: str) -> Dict[str, Any]:
        """
        Recupera todos os resultados de um workflow.

        Args:
            workflow_id: ID do workflow

        Returns:
            Dicionário com todos os resultados
        """
        with self.lock:
            if workflow_id not in self.contexts:
                return {}

            return self.contexts[workflow_id].get("results", {}).copy()

    def add_metadata(
        self,
        workflow_id: str,
        key: str,
        value: Any
    ) -> None:
        """
        Adiciona metadados ao contexto.

        Args:
            workflow_id: ID do workflow
            key: Chave do metadado
            value: Valor do metadado
        """
        with self.lock:
            if workflow_id not in self.contexts:
                raise ValueError(f"Context for workflow {workflow_id} not found")

            if "metadata" not in self.contexts[workflow_id]:
                self.contexts[workflow_id]["metadata"] = {}

            self.contexts[workflow_id]["metadata"][key] = value
            self.contexts[workflow_id]["metadata"]["updated_at"] = datetime.utcnow().isoformat()

    def get_metadata(
        self,
        workflow_id: str,
        key: Optional[str] = None
    ) -> Any:
        """
        Recupera metadados do contexto.

        Args:
            workflow_id: ID do workflow
            key: Chave específica (opcional)

        Returns:
            Metadados ou valor específico
        """
        with self.lock:
            if workflow_id not in self.contexts:
                return None

            metadata = self.contexts[workflow_id].get("metadata", {})

            if key:
                return metadata.get(key)

            return metadata.copy()

    def list_active_contexts(self) -> List[str]:
        """
        Lista contextos ativos.

        Returns:
            Lista de IDs de workflows com contextos ativos
        """
        with self.lock:
            return list(self.contexts.keys())

    def clear_old_contexts(self, max_age_hours: int = 24) -> int:
        """
        Limpa contextos antigos.

        Args:
            max_age_hours: Idade máxima em horas

        Returns:
            Número de contextos removidos
        """
        with self.lock:
            from datetime import timedelta

            cutoff = datetime.utcnow() - timedelta(hours=max_age_hours)
            removed = 0

            for workflow_id in list(self.contexts.keys()):
                updated_str = self.contexts[workflow_id].get("metadata", {}).get("updated_at")
                if updated_str:
                    updated = datetime.fromisoformat(updated_str)
                    if updated < cutoff:
                        self.delete_context(workflow_id)
                        removed += 1

            return removed

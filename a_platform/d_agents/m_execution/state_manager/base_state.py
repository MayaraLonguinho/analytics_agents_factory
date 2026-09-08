"""
Base State Manager - Interface base para gestores de estado
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ...interfaces import IStateManager


class BaseStateManager(IStateManager, ABC):
    """
    Classe base para gestores de estado.
    Implementa funcionalidades comuns de gestão de estado.
    """

    def __init__(self):
        """
        Inicializa o gestor de estado.
        """
        self.cache: Dict[str, Dict[str, Any]] = {}

    def _cache_state(self, workflow_id: str, state: Dict[str, Any]) -> None:
        """
        Cacheia estado na memória.

        Args:
            workflow_id: ID do workflow
            state: Estado a cachear
        """
        self.cache[workflow_id] = state.copy()

    def _get_cached_state(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Recupera estado cacheado.

        Args:
            workflow_id: ID do workflow

        Returns:
            Estado cacheado ou None
        """
        return self.cache.get(workflow_id)

    def _clear_cache(self, workflow_id: str) -> None:
        """
        Limpa cache de um workflow.

        Args:
            workflow_id: ID do workflow
        """
        if workflow_id in self.cache:
            del self.cache[workflow_id]

    def clear_all_cache(self) -> None:
        """Limpa todo o cache."""
        self.cache.clear()

    def get_cached_workflows(self) -> list:
        """
        Retorna workflows cacheados.

        Returns:
            Lista de IDs de workflows cacheados
        """
        return list(self.cache.keys())

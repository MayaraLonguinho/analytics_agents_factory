"""
Interfaces de memória do Analytics AI Factory.

Define os contratos das diferentes formas de memória utilizadas
pelo Brain.

O contrato de storage permanece no Core.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from uuid import UUID

from a_platform.c_brain.memory.schemas import (
    MemoryConfig,
    MemoryQuery,
    MemoryStatistics,
)


class IMemory(ABC):
    """
    Interface base para todos os tipos de memória.
    """

    @abstractmethod
    async def store(
        self,
        key: str,
        value: Any,
        ttl: Optional[float] = None,
    ) -> bool:
        """
        Armazena um valor.
        """
        pass

    @abstractmethod
    async def retrieve(
        self,
        key: str,
    ) -> Optional[Any]:
        """
        Recupera um valor.
        """
        pass

    @abstractmethod
    async def delete(
        self,
        key: str,
    ) -> bool:
        """
        Remove um valor.
        """
        pass

    @abstractmethod
    async def exists(
        self,
        key: str,
    ) -> bool:
        """
        Verifica se uma chave existe.
        """
        pass

    @abstractmethod
    async def clear(self) -> bool:
        """
        Remove todos os valores.
        """
        pass

    @abstractmethod
    async def get_stats(self) -> MemoryStatistics:
        """
        Retorna estatísticas da memória.
        """
        pass

    @abstractmethod
    def get_config(self) -> MemoryConfig:
        """
        Retorna a configuração da memória.
        """
        pass

    @abstractmethod
    async def update_config(
        self,
        config: MemoryConfig,
    ) -> None:
        """
        Atualiza a configuração da memória.
        """
        pass


class IShortTermMemory(IMemory):
    """
    Interface para memória de curto prazo.

    Armazena informações temporárias e de acesso rápido.
    """

    @abstractmethod
    async def store_temporary(
        self,
        key: str,
        value: Any,
        ttl: float,
    ) -> bool:
        pass

    @abstractmethod
    async def retrieve_recent(
        self,
        limit: int = 10,
    ) -> List[Any]:
        pass

    @abstractmethod
    async def cleanup_expired(self) -> int:
        pass

    @abstractmethod
    async def get_ttl(
        self,
        key: str,
    ) -> Optional[float]:
        pass


class ILongTermMemory(IMemory):
    """
    Interface para memória de longo prazo.
    """

    @abstractmethod
    async def store_permanent(
        self,
        key: str,
        value: Any,
    ) -> bool:
        pass

    @abstractmethod
    async def retrieve_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        limit: int = 100,
    ) -> List[Any]:
        pass

    @abstractmethod
    async def retrieve_by_tags(
        self,
        tags: Set[str],
        limit: int = 100,
    ) -> List[Any]:
        pass

    @abstractmethod
    async def archive_old_entries(
        self,
        older_than_days: int = 30,
    ) -> int:
        pass

    @abstractmethod
    async def query(
        self,
        query: MemoryQuery,
    ) -> List[Any]:
        pass


class IConversationMemory(IMemory):
    """
    Interface para memória de conversação.
    """

    @abstractmethod
    async def start_conversation(
        self,
        conversation_id: UUID,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        pass

    @abstractmethod
    async def end_conversation(
        self,
        conversation_id: UUID,
    ) -> bool:
        pass

    @abstractmethod
    async def store_message(
        self,
        conversation_id: UUID,
        message: Any,
        sequence: int,
    ) -> bool:
        pass

    @abstractmethod
    async def get_conversation_history(
        self,
        conversation_id: UUID,
        limit: Optional[int] = None,
    ) -> List[Any]:
        pass

    @abstractmethod
    async def list_conversations(
        self,
        active_only: bool = False,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_conversation_metadata(
        self,
        conversation_id: UUID,
    ) -> Optional[Dict[str, Any]]:
        pass


class IExecutionMemory(IMemory):
    """
    Interface para memória de execução.
    """

    @abstractmethod
    async def start_execution(
        self,
        execution_id: UUID,
        agent_name: str,
        skill_name: str,
        input_data: Dict[str, Any],
    ) -> bool:
        pass

    @abstractmethod
    async def end_execution(
        self,
        execution_id: UUID,
        output_data: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
    ) -> bool:
        pass

    @abstractmethod
    async def store_execution_state(
        self,
        execution_id: UUID,
        state: Dict[str, Any],
    ) -> bool:
        pass

    @abstractmethod
    async def get_execution_state(
        self,
        execution_id: UUID,
    ) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def list_active_executions(
        self,
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_execution_history(
        self,
        execution_id: UUID,
    ) -> List[Dict[str, Any]]:
        pass


class ISkillMemory(IMemory):
    """
    Interface para memória de resultados de Skills.
    """

    @abstractmethod
    async def store_skill_result(
        self,
        skill: str,
        key: str,
        result: Any,
        ttl: Optional[float] = None,
    ) -> bool:
        pass

    @abstractmethod
    async def retrieve_skill_result(
        self,
        skill: str,
        key: str,
    ) -> Optional[Any]:
        pass

    @abstractmethod
    async def invalidate_skill(
        self,
        skill: str,
    ) -> int:
        pass

    @abstractmethod
    async def get_skill_stats(
        self,
        skill: str,
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def list_skills(self) -> List[str]:
        pass


class IArchitectureMemory(IMemory):
    """
    Interface para memória de arquitetura de projetos.
    """

    @abstractmethod
    async def store_architecture(
        self,
        project_id: str,
        architecture: Dict[str, Any],
        version: str,
    ) -> bool:
        pass

    @abstractmethod
    async def retrieve_architecture(
        self,
        project_id: str,
        version: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def store_decision(
        self,
        project_id: str,
        decision: Dict[str, Any],
    ) -> bool:
        pass

    @abstractmethod
    async def get_architecture_history(
        self,
        project_id: str,
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def list_projects(self) -> List[str]:
        pass

    @abstractmethod
    async def get_project_decisions(
        self,
        project_id: str,
    ) -> List[Dict[str, Any]]:
        pass
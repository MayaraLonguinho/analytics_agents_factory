"""
Memory Manager - Coordenador central de tipos de memória
"""

from typing import Any, Dict, List, Optional, Set
from uuid import UUID
from datetime import datetime
from .interfaces import (
    IShortTermMemory,
    ILongTermMemory,
    IConversationMemory,
    IExecutionMemory,
    ISkillMemory,
    IArchitectureMemory
)
from .a_short_term import ShortTermMemory
from .b_long_term import LongTermMemory
from .c_conversation import ConversationMemory
from .d_execution import ExecutionMemory
from .e_skill import SkillMemory
from .f_architecture import ArchitectureMemory
from a_platform.c_brain.e_memory.schemas import (
    MemoryType,
    MemoryStatistics,
    MemoryConfig,
    MemoryQuery
)


class MemoryManager:
    """
    Coordenador central que gerencia todos os tipos de memória.
    Fornece interface unificada para acesso a diferentes tipos de memória.
    """

    def __init__(self):
        """Inicializa o Memory Manager com todos os tipos de memória."""
        self.short_term_memory: IShortTermMemory = ShortTermMemory()
        self.long_term_memory: ILongTermMemory = LongTermMemory()
        self.conversation_memory: IConversationMemory = ConversationMemory()
        self.execution_memory: IExecutionMemory = ExecutionMemory()
        self.skill_memory: ISkillMemory = SkillMemory()
        self.architecture_memory: IArchitectureMemory = ArchitectureMemory()

        # Mapeamento de tipo de memória para implementação
        self._memory_map = {
            MemoryType.SHORT_TERM: self.short_term_memory,
            MemoryType.LONG_TERM: self.long_term_memory,
            MemoryType.CONVERSATION: self.conversation_memory,
            MemoryType.EXECUTION: self.execution_memory,
            MemoryType.SKILL: self.skill_memory,
            MemoryType.ARCHITECTURE: self.architecture_memory
        }

    # ========================================================================
    # Métodos Genéricos
    # ========================================================================

    async def store(
        self,
        memory_type: MemoryType,
        key: str,
        value: Any,
        ttl: Optional[float] = None
    ) -> bool:
        """
        Armazena um valor em um tipo específico de memória.

        Args:
            memory_type: Tipo de memória
            key: Chave única
            value: Valor a armazenar
            ttl: Time-to-live em segundos

        Returns:
            True se armazenado com sucesso
        """
        memory = self._memory_map.get(memory_type)
        if not memory:
            raise ValueError(f"Unknown memory type: {memory_type}")
        return await memory.store(key, value, ttl)

    async def retrieve(self, memory_type: MemoryType, key: str) -> Optional[Any]:
        """
        Recupera um valor de um tipo específico de memória.

        Args:
            memory_type: Tipo de memória
            key: Chave a buscar

        Returns:
            Valor armazenado ou None
        """
        memory = self._memory_map.get(memory_type)
        if not memory:
            raise ValueError(f"Unknown memory type: {memory_type}")
        return await memory.retrieve(key)

    async def delete(self, memory_type: MemoryType, key: str) -> bool:
        """
        Remove um valor de um tipo específico de memória.

        Args:
            memory_type: Tipo de memória
            key: Chave a remover

        Returns:
            True se removido com sucesso
        """
        memory = self._memory_map.get(memory_type)
        if not memory:
            raise ValueError(f"Unknown memory type: {memory_type}")
        return await memory.delete(key)

    async def exists(self, memory_type: MemoryType, key: str) -> bool:
        """
        Verifica se uma chave existe em um tipo específico de memória.

        Args:
            memory_type: Tipo de memória
            key: Chave a verificar

        Returns:
            True se a chave existe
        """
        memory = self._memory_map.get(memory_type)
        if not memory:
            raise ValueError(f"Unknown memory type: {memory_type}")
        return await memory.exists(key)

    async def clear(self, memory_type: MemoryType) -> bool:
        """
        Limpa todos os valores de um tipo específico de memória.

        Args:
            memory_type: Tipo de memória

        Returns:
            True se limpo com sucesso
        """
        memory = self._memory_map.get(memory_type)
        if not memory:
            raise ValueError(f"Unknown memory type: {memory_type}")
        return await memory.clear()

    async def get_stats(self, memory_type: MemoryType) -> MemoryStatistics:
        """
        Retorna estatísticas de um tipo específico de memória.

        Args:
            memory_type: Tipo de memória

        Returns:
            MemoryStatistics
        """
        memory = self._memory_map.get(memory_type)
        if not memory:
            raise ValueError(f"Unknown memory type: {memory_type}")
        return await memory.get_stats()

    async def get_all_stats(self) -> Dict[MemoryType, MemoryStatistics]:
        """
        Retorna estatísticas de todos os tipos de memória.

        Returns:
            Dicionário mapeando tipo de memória para estatísticas
        """
        stats = {}
        for memory_type, memory in self._memory_map.items():
            stats[memory_type] = await memory.get_stats()
        return stats

    # ========================================================================
    # Short Term Memory Methods
    # ========================================================================

    async def store_temporary(self, key: str, value: Any, ttl: float) -> bool:
        """Armazena um valor temporário com TTL obrigatório."""
        return await self.short_term_memory.store_temporary(key, value, ttl)

    async def retrieve_recent(self, limit: int = 10) -> List[Any]:
        """Recupera os valores mais recentes do STM."""
        return await self.short_term_memory.retrieve_recent(limit)

    async def cleanup_expired_stm(self) -> int:
        """Remove entradas expiradas do STM."""
        return await self.short_term_memory.cleanup_expired()

    # ========================================================================
    # Long Term Memory Methods
    # ========================================================================

    async def store_permanent(self, key: str, value: Any) -> bool:
        """Armazena um valor permanentemente no LTM."""
        return await self.long_term_memory.store_permanent(key, value)

    async def retrieve_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        limit: int = 100
    ) -> List[Any]:
        """Recupera valores do LTM por range de data."""
        return await self.long_term_memory.retrieve_by_date_range(start_date, end_date, limit)

    async def retrieve_by_tags(self, tags: Set[str], limit: int = 100) -> List[Any]:
        """Recupera valores do LTM por tags."""
        return await self.long_term_memory.retrieve_by_tags(tags, limit)

    async def archive_old_entries(self, older_than_days: int = 30) -> int:
        """Arquiva entradas antigas do LTM."""
        return await self.long_term_memory.archive_old_entries(older_than_days)

    async def query_ltm(self, query: MemoryQuery) -> List[Any]:
        """Executa uma query complexa no LTM."""
        return await self.long_term_memory.query(query)

    # ========================================================================
    # Conversation Memory Methods
    # ========================================================================

    async def start_conversation(
        self,
        conversation_id: UUID,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Inicia uma nova conversa."""
        return await self.conversation_memory.start_conversation(conversation_id, metadata)

    async def end_conversation(self, conversation_id: UUID) -> bool:
        """Encerra uma conversa."""
        return await self.conversation_memory.end_conversation(conversation_id)

    async def store_message(
        self,
        conversation_id: UUID,
        message: Any,
        sequence: int
    ) -> bool:
        """Armazena uma mensagem em uma conversa."""
        return await self.conversation_memory.store_message(conversation_id, message, sequence)

    async def get_conversation_history(
        self,
        conversation_id: UUID,
        limit: Optional[int] = None
    ) -> List[Any]:
        """Recupera o histórico de uma conversa."""
        return await self.conversation_memory.get_conversation_history(conversation_id, limit)

    async def list_conversations(
        self,
        active_only: bool = False,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Lista conversas."""
        return await self.conversation_memory.list_conversations(active_only, limit)

    async def get_conversation_metadata(
        self,
        conversation_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """Recupera metadados de uma conversa."""
        return await self.conversation_memory.get_conversation_metadata(conversation_id)

    # ========================================================================
    # Execution Memory Methods
    # ========================================================================

    async def start_execution(
        self,
        execution_id: UUID,
        agent_name: str,
        skill_name: str,
        input_data: Dict[str, Any]
    ) -> bool:
        """Inicia uma execução."""
        return await self.execution_memory.start_execution(
            execution_id, agent_name, skill_name, input_data
        )

    async def end_execution(
        self,
        execution_id: UUID,
        output_data: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None
    ) -> bool:
        """Encerra uma execução."""
        return await self.execution_memory.end_execution(
            execution_id, output_data, error_message
        )

    async def store_execution_state(
        self,
        execution_id: UUID,
        state: Dict[str, Any]
    ) -> bool:
        """Armazena o estado de uma execução."""
        return await self.execution_memory.store_execution_state(execution_id, state)

    async def get_execution_state(self, execution_id: UUID) -> Optional[Dict[str, Any]]:
        """Recupera o estado de uma execução."""
        return await self.execution_memory.get_execution_state(execution_id)

    async def list_active_executions(self) -> List[Dict[str, Any]]:
        """Lista execuções ativas."""
        return await self.execution_memory.list_active_executions()

    async def get_execution_history(self, execution_id: UUID) -> List[Dict[str, Any]]:
        """Recupera o histórico de uma execução."""
        return await self.execution_memory.get_execution_history(execution_id)

    # ========================================================================
    # Skill Memory Methods
    # ========================================================================

    async def store_skill_result(
        self,
        skill: str,
        key: str,
        result: Any,
        ttl: Optional[float] = None
    ) -> bool:
        """Armazena resultado de uma skill."""
        return await self.skill_memory.store_skill_result(skill, key, result, ttl)

    async def retrieve_skill_result(self, skill: str, key: str) -> Optional[Any]:
        """Recupera resultado de uma skill."""
        return await self.skill_memory.retrieve_skill_result(skill, key)

    async def invalidate_skill(self, skill: str) -> int:
        """Invalida todos os resultados de uma skill."""
        return await self.skill_memory.invalidate_skill(skill)

    async def get_skill_stats(self, skill: str) -> Dict[str, Any]:
        """Retorna estatísticas de uma skill."""
        return await self.skill_memory.get_skill_stats(skill)

    async def list_skills(self) -> List[str]:
        """Lista skills com dados armazenados."""
        return await self.skill_memory.list_skills()

    # ========================================================================
    # Architecture Memory Methods
    # ========================================================================

    async def store_architecture(
        self,
        project_id: str,
        architecture: Dict[str, Any],
        version: str
    ) -> bool:
        """Armazena arquitetura de um projeto."""
        return await self.architecture_memory.store_architecture(
            project_id, architecture, version
        )

    async def retrieve_architecture(
        self,
        project_id: str,
        version: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Recupera arquitetura de um projeto."""
        return await self.architecture_memory.retrieve_architecture(project_id, version)

    async def store_decision(
        self,
        project_id: str,
        decision: Dict[str, Any]
    ) -> bool:
        """Armazena uma decisão arquitetural."""
        return await self.architecture_memory.store_decision(project_id, decision)

    async def get_architecture_history(self, project_id: str) -> List[Dict[str, Any]]:
        """Recupera histórico de versões da arquitetura."""
        return await self.architecture_memory.get_architecture_history(project_id)

    async def list_projects(self) -> List[str]:
        """Lista todos os projetos."""
        return await self.architecture_memory.list_projects()

    async def get_project_decisions(self, project_id: str) -> List[Dict[str, Any]]:
        """Recupera decisões de um projeto."""
        return await self.architecture_memory.get_project_decisions(project_id)

    # ========================================================================
    # Métodos de Configuração
    # ========================================================================

    def get_memory_config(self, memory_type: MemoryType) -> MemoryConfig:
        """Retorna a configuração de um tipo de memória."""
        memory = self._memory_map.get(memory_type)
        if not memory:
            raise ValueError(f"Unknown memory type: {memory_type}")
        return memory.get_config()

    async def update_memory_config(
        self,
        memory_type: MemoryType,
        config: MemoryConfig
    ) -> None:
        """Atualiza a configuração de um tipo de memória."""
        memory = self._memory_map.get(memory_type)
        if not memory:
            raise ValueError(f"Unknown memory type: {memory_type}")
        await memory.update_config(config)

    # ========================================================================
    # Métodos de Limpeza Global
    # ========================================================================

    async def clear_all(self) -> Dict[MemoryType, bool]:
        """
        Limpa todos os tipos de memória.

        Returns:
            Dicionário mapeando tipo de memória para resultado
        """
        results = {}
        for memory_type, memory in self._memory_map.items():
            results[memory_type] = await memory.clear()
        return results

    async def cleanup_all_expired(self) -> Dict[MemoryType, int]:
        """
        Remove entradas expiradas de todos os tipos de memória.

        Returns:
            Dicionário mapeando tipo de memória para número de entradas removidas
        """
        results = {}
        for memory_type, memory in self._memory_map.items():
            if hasattr(memory, 'cleanup_expired'):
                results[memory_type] = await memory.cleanup_expired()
            else:
                results[memory_type] = 0
        return results

"""
Short Term Memory - Implementação de memória de curto prazo
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from uuid import uuid4
from ..interfaces import IShortTermMemory
from a_platform.c_brain.e_memory.storage import InMemoryStorage
from a_platform.c_brain.e_memory.schemas import (
    MemoryEntry,
    MemoryType,
    DataType,
    EntryStatus,
    MemoryStatistics,
    MemoryConfig
)


class ShortTermMemory(IShortTermMemory):
    """
    Implementação de Short Term Memory.
    Memória volátil e rápida para dados temporários.
    """

    def __init__(self, config: Optional[MemoryConfig] = None):
        """
        Inicializa a Short Term Memory.

        Args:
            config: Configuração da memória
        """
        self.config = config or MemoryConfig(
            max_entries=1000,
            default_ttl=300.0,  # 5 minutos
            eviction_policy="lru"
        )
        self.storage = InMemoryStorage(max_size_mb=100)
        self.entries: Dict[str, MemoryEntry] = {}

    async def store(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        """Armazena um valor."""
        entry = MemoryEntry(
            key=key,
            value=value,
            memory_type=MemoryType.SHORT_TERM,
            data_type=DataType.CACHE,
            ttl=ttl or self.config.default_ttl,
            expires_at=datetime.utcnow() + timedelta(seconds=ttl or self.config.default_ttl) if ttl else None
        )

        success = await self.storage.store(key, entry, ttl)
        if success:
            self.entries[key] = entry
        return success

    async def retrieve(self, key: str) -> Optional[Any]:
        """Recupera um valor."""
        entry = await self.storage.retrieve(key)
        if entry:
            return entry.value
        return None

    async def delete(self, key: str) -> bool:
        """Remove um valor."""
        success = await self.storage.delete(key)
        if success and key in self.entries:
            del self.entries[key]
        return success

    async def exists(self, key: str) -> bool:
        """Verifica se uma chave existe."""
        return await self.storage.exists(key)

    async def clear(self) -> bool:
        """Limpa todos os valores."""
        success = await self.storage.clear()
        self.entries.clear()
        return success

    async def get_stats(self) -> MemoryStatistics:
        """Retorna estatísticas."""
        storage_stats = await self.storage.get_stats()

        return MemoryStatistics(
            total_entries=storage_stats["total_entries"],
            active_entries=storage_stats["total_entries"],
            archived_entries=0,
            expired_entries=storage_stats["entries_with_ttl"],
            total_size_bytes=storage_stats["total_size_bytes"],
            average_access_count=storage_stats["total_access_count"] / storage_stats["total_entries"] if storage_stats["total_entries"] > 0 else 0.0
        )

    def get_config(self) -> MemoryConfig:
        """Retorna a configuração."""
        return self.config

    async def update_config(self, config: MemoryConfig) -> None:
        """Atualiza a configuração."""
        self.config = config

    async def store_temporary(self, key: str, value: Any, ttl: float) -> bool:
        """Armazena um valor temporário com TTL obrigatório."""
        return await self.store(key, value, ttl)

    async def retrieve_recent(self, limit: int = 10) -> List[Any]:
        """Recupera os valores mais recentes."""
        keys = await self.storage.keys()
        recent_keys = sorted(keys, key=lambda k: self.entries[k].created_at, reverse=True)[:limit]
        return [self.entries[k].value for k in recent_keys if k in self.entries]

    async def cleanup_expired(self) -> int:
        """Remove entradas expiradas."""
        removed = await self.storage.cleanup_expired()
        for key in list(self.entries.keys()):
            if self.entries[key].is_expired():
                del self.entries[key]
        return removed

    async def get_ttl(self, key: str) -> Optional[float]:
        """Retorna o TTL restante de uma chave."""
        entry = self.entries.get(key)
        if entry and entry.expires_at:
            remaining = (entry.expires_at - datetime.utcnow()).total_seconds()
            return max(0, remaining)
        return None

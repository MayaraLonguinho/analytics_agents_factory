"""
Long Term Memory - Implementação de memória de longo prazo
"""

from typing import Any, Dict, List, Optional, Set
from datetime import datetime, timedelta
from ..interfaces import ILongTermMemory
from a_platform.c_brain.memory.storage import InMemoryStorage
from a_platform.c_brain.memory.schemas import (
    MemoryEntry,
    MemoryType,
    DataType,
    MemoryStatistics,
    MemoryConfig,
    MemoryQuery
)


class LongTermMemory(ILongTermMemory):
    """Implementação de Long Term Memory com storage abstrato."""

    def __init__(self, config: Optional[MemoryConfig] = None):
        self.config = config or MemoryConfig(max_entries=100000)
        self.storage = InMemoryStorage(max_size_mb=500)

    async def store(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        entry = MemoryEntry(key=key, value=value, memory_type=MemoryType.LONG_TERM, data_type=DataType.HISTORY)
        return await self.storage.store(key, entry)

    async def retrieve(self, key: str) -> Optional[Any]:
        entry = await self.storage.retrieve(key)
        return entry.value if entry else None

    async def delete(self, key: str) -> bool:
        return await self.storage.delete(key)

    async def exists(self, key: str) -> bool:
        return await self.storage.exists(key)

    async def clear(self) -> bool:
        return await self.storage.clear()

    async def get_stats(self) -> MemoryStatistics:
        stats = await self.storage.get_stats()
        return MemoryStatistics(total_entries=stats["total_entries"], active_entries=stats["total_entries"], total_size_bytes=stats["total_size_bytes"])

    def get_config(self) -> MemoryConfig:
        return self.config

    async def update_config(self, config: MemoryConfig) -> None:
        self.config = config

    async def store_permanent(self, key: str, value: Any) -> bool:
        return await self.store(key, value, ttl=None)

    async def retrieve_by_date_range(self, start_date: datetime, end_date: datetime, limit: int = 100) -> List[Any]:
        keys = await self.storage.keys()
        filtered = []
        for key in keys:
            entry = await self.storage.retrieve(key)
            if entry and start_date <= entry.created_at <= end_date:
                filtered.append(entry.value)
                if len(filtered) >= limit:
                    break
        return filtered

    async def retrieve_by_tags(self, tags: Set[str], limit: int = 100) -> List[Any]:
        keys = await self.storage.keys()
        filtered = []
        for key in keys:
            entry = await self.storage.retrieve(key)
            if entry and tags.issubset(entry.tags):
                filtered.append(entry.value)
                if len(filtered) >= limit:
                    break
        return filtered

    async def archive_old_entries(self, older_than_days: int = 30) -> int:
        cutoff = datetime.utcnow() - timedelta(days=older_than_days)
        keys = await self.storage.keys()
        archived = 0
        for key in keys:
            entry = await self.storage.retrieve(key)
            if entry and entry.created_at < cutoff:
                entry.status = EntryStatus.ARCHIVED
                archived += 1
        return archived

    async def query(self, query: MemoryQuery) -> List[Any]:
        keys = await self.storage.keys()
        results = []
        for key in keys:
            entry = await self.storage.retrieve(key)
            if entry and self._matches_query(entry, query):
                results.append(entry.value)
                if len(results) >= query.limit:
                    break
        return results

    def _matches_query(self, entry: MemoryEntry, query: MemoryQuery) -> bool:
        if query.memory_type and entry.memory_type != query.memory_type:
            return False
        if query.data_type and entry.data_type != query.data_type:
            return False
        if query.tags and not query.tags.issubset(entry.tags):
            return False
        if query.status and entry.status != query.status:
            return False
        if query.created_after and entry.created_at < query.created_after:
            return False
        if query.created_before and entry.created_at > query.created_before:
            return False
        if query.key_pattern and query.key_pattern not in entry.key:
            return False
        return True

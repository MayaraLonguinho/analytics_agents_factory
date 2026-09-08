from typing import Any, Optional
from a_platform.c_brain.e_memory.schemas import MemoryStatistics

class InMemoryStorage:
    def __init__(self, max_size_mb: Optional[int] = None):
        self.max_size_mb = max_size_mb
        self.data = {}

    async def store(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        self.data[key] = value
        return True

    async def retrieve(self, key: str) -> Optional[Any]:
        return self.data.get(key)

    async def delete(self, key: str) -> bool:
        if key in self.data:
            del self.data[key]
            return True
        return False

    async def exists(self, key: str) -> bool:
        return key in self.data

    async def clear(self) -> bool:
        self.data.clear()
        return True

    async def get_stats(self) -> MemoryStatistics:
        return MemoryStatistics(entries_count=len(self.data), total_size_mb=0.0)

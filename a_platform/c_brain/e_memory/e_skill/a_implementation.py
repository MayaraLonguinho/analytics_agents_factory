"""
Skill Memory - Implementação de memória de skills
"""

from typing import Any, Dict, List, Optional
from ..k_interfaces import ISkillMemory
from a_platform.c_brain.e_memory.q_storage import InMemoryStorage
from a_platform.c_brain.e_memory.b_memory_schema import (
    MemoryEntry,
    MemoryType,
    DataType,
    MemoryStatistics,
    MemoryConfig
)


class SkillMemory(ISkillMemory):
    """Implementação de Skill Memory para cache de resultados."""

    def __init__(self, config: Optional[MemoryConfig] = None):
        self.config = config or MemoryConfig(default_ttl=1800.0)  # 30 minutos
        self.storage = InMemoryStorage(max_size_mb=200)
        self.skill_stats: Dict[str, Dict[str, int]] = {}

    async def store(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        entry = MemoryEntry(key=key, value=value, memory_type=MemoryType.SKILL, data_type=DataType.RESULT)
        return await self.storage.store(key, entry, ttl)

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

    async def store_skill_result(self, skill: str, key: str, result: Any, ttl: Optional[float] = None) -> bool:
        storage_key = f"{skill}:{key}"
        success = await self.store(storage_key, result, ttl)
        if success:
            self.skill_stats.setdefault(skill, {"stored": 0, "retrieved": 0, "misses": 0})
            self.skill_stats[skill]["stored"] += 1
        return success

    async def retrieve_skill_result(self, skill: str, key: str) -> Optional[Any]:
        storage_key = f"{skill}:{key}"
        result = await self.retrieve(storage_key)
        if result is not None:
            self.skill_stats.setdefault(skill, {"stored": 0, "retrieved": 0, "misses": 0})
            self.skill_stats[skill]["retrieved"] += 1
        else:
            self.skill_stats.setdefault(skill, {"stored": 0, "retrieved": 0, "misses": 0})
            self.skill_stats[skill]["misses"] += 1
        return result

    async def invalidate_skill(self, skill: str) -> int:
        keys = await self.storage.keys()
        pattern = f"{skill}:"
        invalidated = 0
        for key in keys:
            if key.startswith(pattern):
                await self.storage.delete(key)
                invalidated += 1
        if skill in self.skill_stats:
            self.skill_stats[skill]["stored"] = 0
            self.skill_stats[skill]["retrieved"] = 0
        return invalidated

    async def get_skill_stats(self, skill: str) -> Dict[str, Any]:
        if skill in self.skill_stats:
            stats = self.skill_stats[skill]
            total = stats["retrieved"] + stats["misses"]
            hit_rate = stats["retrieved"] / total if total > 0 else 0.0
            return {
                "skill": skill,
                "stored": stats["stored"],
                "retrieved": stats["retrieved"],
                "misses": stats["misses"],
                "hit_rate": hit_rate
            }
        return {"skill": skill, "stored": 0, "retrieved": 0, "misses": 0, "hit_rate": 0.0}

    async def list_skills(self) -> List[str]:
        return list(self.skill_stats.keys())

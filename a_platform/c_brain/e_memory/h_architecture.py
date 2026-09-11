"""
Architecture Memory - Implementação de memória de arquitetura
"""

from typing import Any, Dict, List, Optional
from ..f_interfaces import IArchitectureMemory
from a_platform.c_brain.e_memory.q_storage import InMemoryStorage
from a_platform.c_brain.e_memory.n_schemas import (
    MemoryEntry,
    MemoryType,
    DataType,
    MemoryStatistics,
    MemoryConfig,
    ArchitectureEntry
)


class ArchitectureMemory(IArchitectureMemory):
    """Implementação de Architecture Memory."""

    def __init__(self, config: Optional[MemoryConfig] = None):
        self.config = config or MemoryConfig()
        self.storage = InMemoryStorage(max_size_mb=200)
        self.projects: Dict[str, Dict[str, Any]] = {}

    async def store(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        entry = MemoryEntry(key=key, value=value, memory_type=MemoryType.ARCHITECTURE, data_type=DataType.ARCHITECTURE)
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

    async def store_architecture(self, project_id: str, architecture: Dict[str, Any], version: str) -> bool:
        storage_key = f"architecture:{project_id}:{version}"
        entry = ArchitectureEntry(
            key=storage_key,
            value=architecture,
            memory_type=MemoryType.ARCHITECTURE,
            data_type=DataType.ARCHITECTURE,
            project_id=project_id,
            component_type="architecture",
            component_name="main",
            version=version,
            architecture_data=architecture
        )
        success = await self.storage.store(storage_key, entry)
        if success:
            self.projects.setdefault(project_id, {"versions": [], "decisions": []})
            self.projects[project_id]["versions"].append(version)
        return success

    async def retrieve_architecture(self, project_id: str, version: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if version:
            storage_key = f"architecture:{project_id}:{version}"
        else:
            # Recuperar última versão
            if project_id in self.projects and self.projects[project_id]["versions"]:
                version = self.projects[project_id]["versions"][-1]
                storage_key = f"architecture:{project_id}:{version}"
            else:
                return None
        entry = await self.storage.retrieve(storage_key)
        return entry.value if entry else None

    async def store_decision(self, project_id: str, decision: Dict[str, Any]) -> bool:
        decision_id = decision.get('decision_id', str(hash(str(decision))))
        storage_key = f"decision:{project_id}:{decision_id}"
        success = await self.storage.store(storage_key, decision)
        if success:
            self.projects.setdefault(project_id, {"versions": [], "decisions": []})
            self.projects[project_id]["decisions"].append(decision)
        return success

    async def get_architecture_history(self, project_id: str) -> List[Dict[str, Any]]:
        if project_id not in self.projects:
            return []
        versions = self.projects[project_id]["versions"]
        history = []
        for version in versions:
            storage_key = f"architecture:{project_id}:{version}"
            entry = await self.storage.retrieve(storage_key)
            if entry:
                history.append(entry.value)
        return history

    async def list_projects(self) -> List[str]:
        return list(self.projects.keys())

    async def get_project_decisions(self, project_id: str) -> List[Dict[str, Any]]:
        if project_id in self.projects:
            return self.projects[project_id]["decisions"]
        return []

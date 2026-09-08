"""
Execution Memory - Implementação de memória de execução
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from datetime import datetime
from ..interfaces import IExecutionMemory
from a_platform.c_brain.memory.storage import InMemoryStorage
from a_platform.c_brain.memory.schemas import (
    MemoryEntry,
    MemoryType,
    DataType,
    MemoryStatistics,
    MemoryConfig,
    ExecutionEntry
)


class ExecutionMemory(IExecutionMemory):
    """Implementação de Execution Memory."""

    def __init__(self, config: Optional[MemoryConfig] = None):
        self.config = config or MemoryConfig()
        self.storage = InMemoryStorage(max_size_mb=100)
        self.executions: Dict[UUID, Dict[str, Any]] = {}

    async def store(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        entry = MemoryEntry(key=key, value=value, memory_type=MemoryType.EXECUTION, data_type=DataType.EXECUTION)
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

    async def start_execution(self, execution_id: UUID, agent_name: str, skill_name: str, input_data: Dict[str, Any]) -> bool:
        self.executions[execution_id] = {
            "execution_id": execution_id,
            "agent_name": agent_name,
            "skill_name": skill_name,
            "input_data": input_data,
            "start_time": datetime.utcnow(),
            "status": "running",
            "state_history": [],
            "output_data": None,
            "error_message": None,
            "retry_count": 0
        }
        return True

    async def end_execution(self, execution_id: UUID, output_data: Optional[Dict[str, Any]] = None, error_message: Optional[str] = None) -> bool:
        if execution_id not in self.executions:
            return False
        self.executions[execution_id]["end_time"] = datetime.utcnow()
        self.executions[execution_id]["output_data"] = output_data
        self.executions[execution_id]["error_message"] = error_message
        self.executions[execution_id]["status"] = "completed" if not error_message else "failed"
        return True

    async def store_execution_state(self, execution_id: UUID, state: Dict[str, Any]) -> bool:
        if execution_id not in self.executions:
            return False
        self.executions[execution_id]["state_history"].append({
            "timestamp": datetime.utcnow(),
            "state": state
        })
        return True

    async def get_execution_state(self, execution_id: UUID) -> Optional[Dict[str, Any]]:
        if execution_id in self.executions:
            return self.executions[execution_id]
        return None

    async def list_active_executions(self) -> List[Dict[str, Any]]:
        active = []
        for exec_id, exec_data in self.executions.items():
            if exec_data["status"] == "running":
                active.append({
                    "execution_id": str(exec_id),
                    "agent_name": exec_data["agent_name"],
                    "skill_name": exec_data["skill_name"],
                    "start_time": exec_data["start_time"],
                    "input_data": exec_data["input_data"]
                })
        return active

    async def get_execution_history(self, execution_id: UUID) -> List[Dict[str, Any]]:
        if execution_id in self.executions:
            return self.executions[execution_id]["state_history"]
        return []

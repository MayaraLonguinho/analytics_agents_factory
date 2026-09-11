"""
Conversation Memory - Implementação de memória de conversação
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from datetime import datetime
from ..f_interfaces import IConversationMemory
from a_platform.c_brain.e_memory.q_storage import InMemoryStorage
from a_platform.c_brain.e_memory.n_schemas import (
    MemoryEntry,
    MemoryType,
    DataType,
    MemoryStatistics,
    MemoryConfig,
    MessageEntry
)


class ConversationMemory(IConversationMemory):
    """Implementação de Conversation Memory."""

    def __init__(self, config: Optional[MemoryConfig] = None):
        self.config = config or MemoryConfig()
        self.storage = InMemoryStorage(max_size_mb=200)
        self.conversations: Dict[UUID, Dict[str, Any]] = {}

    async def store(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        entry = MemoryEntry(key=key, value=value, memory_type=MemoryType.CONVERSATION, data_type=DataType.MESSAGE)
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

    async def start_conversation(self, conversation_id: UUID, metadata: Optional[Dict[str, Any]] = None) -> bool:
        self.conversations[conversation_id] = {
            "started_at": datetime.utcnow(),
            "metadata": metadata or {},
            "messages": [],
            "active": True
        }
        return True

    async def end_conversation(self, conversation_id: UUID) -> bool:
        if conversation_id in self.conversations:
            self.conversations[conversation_id]["active"] = False
            self.conversations[conversation_id]["ended_at"] = datetime.utcnow()
            return True
        return False

    async def store_message(self, conversation_id: UUID, message: Any, sequence: int) -> bool:
        if conversation_id not in self.conversations:
            await self.start_conversation(conversation_id)
        self.conversations[conversation_id]["messages"].append({
            "sequence": sequence,
            "message": message,
            "timestamp": datetime.utcnow()
        })
        return True

    async def get_conversation_history(self, conversation_id: UUID, limit: Optional[int] = None) -> List[Any]:
        if conversation_id not in self.conversations:
            return []
        messages = self.conversations[conversation_id]["messages"]
        if limit:
            return [m["message"] for m in messages[-limit:]]
        return [m["message"] for m in messages]

    async def list_conversations(self, active_only: bool = False, limit: int = 100) -> List[Dict[str, Any]]:
        conversations = []
        for conv_id, conv_data in list(self.conversations.items())[:limit]:
            if active_only and not conv_data["active"]:
                continue
            conversations.append({
                "conversation_id": str(conv_id),
                "started_at": conv_data["started_at"],
                "active": conv_data["active"],
                "message_count": len(conv_data["messages"]),
                "metadata": conv_data["metadata"]
            })
        return conversations

    async def get_conversation_metadata(self, conversation_id: UUID) -> Optional[Dict[str, Any]]:
        if conversation_id in self.conversations:
            return self.conversations[conversation_id].get("metadata")
        return None

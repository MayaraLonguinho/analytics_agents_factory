"""
Sistema de memória do Brain do Analytics AI Factory.
"""

from .interfaces import (
    IArchitectureMemory,
    IConversationMemory,
    IExecutionMemory,
    ILongTermMemory,
    IMemory,
    IShortTermMemory,
    ISkillMemory,
)

from .memory_manager import MemoryManager

__all__ = [
    "IMemory",
    "IShortTermMemory",
    "ILongTermMemory",
    "IConversationMemory",
    "IExecutionMemory",
    "ISkillMemory",
    "IArchitectureMemory",
    "MemoryManager",
]
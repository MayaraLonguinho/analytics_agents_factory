"""
Sistema de memória do Brain do Analytics AI Factory.
"""

from .k_interfaces import (
    IArchitectureMemory,
    IConversationMemory,
    IExecutionMemory,
    ILongTermMemory,
    IMemory,
    IShortTermMemory,
    ISkillMemory,
)

from .a_memory_manager import MemoryManager

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
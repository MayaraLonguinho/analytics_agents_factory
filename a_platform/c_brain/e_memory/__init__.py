"""
Sistema de memória do Brain do Analytics AI Factory.
"""

from .f_interfaces import (
    IArchitectureMemory,
    IConversationMemory,
    IExecutionMemory,
    ILongTermMemory,
    IMemory,
    IShortTermMemory,
    ISkillMemory,
)

from .m_memory_manager import MemoryManager

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
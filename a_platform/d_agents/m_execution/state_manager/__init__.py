"""
State Manager Module - Gestão de estado do Orchestrator Agent
"""

from .base_state import BaseStateManager
from .file_state import FileStateManager

__all__ = ['BaseStateManager', 'FileStateManager']

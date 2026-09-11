"""
State Manager Module - Gestão de estado do Orchestrator Agent
"""

from .a_base_state import BaseStateManager
from .b_file_state import FileStateManager

__all__ = ['BaseStateManager', 'FileStateManager']

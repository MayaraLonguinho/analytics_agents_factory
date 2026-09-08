"""
Dispatcher Module - Despacho de agentes do Orchestrator Agent
"""

from .base_dispatcher import BaseDispatcher
from .agent_dispatcher import AgentDispatcher

__all__ = ['BaseDispatcher', 'AgentDispatcher']

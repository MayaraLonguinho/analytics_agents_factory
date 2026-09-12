"""Canonical MCP registry and executor for Analytics AI Factory.

This module consolidates all configured MCPs behind a single registry and executor.
Agents and Skills must go through this package instead of importing tool-specific
implementations directly.
"""

from .d_registry.a_registry import MCPDefinition, MCPRegistry
from .e_executor.a_executor import MCPExecutor

__all__ = ["MCPDefinition", "MCPRegistry", "MCPExecutor"]

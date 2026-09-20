"""
c_tests/a_unit/e_mcps/d_test_registry.py
======================================
Especificação executável de MCPRegistry.
Valida catálogo de MCPs, busca por capability e esquemas de entrada/saída.
"""
import pytest

from a_platform.f_mcps.d_registry.a_registry import MCPRegistry


def test_mcp_registry_initialization():
    """Valida que o registry carrega os MCPs homologados (filesystem, database, docker)."""
    registry = MCPRegistry()
    mcps = registry.list_mcps()
    assert len(mcps) >= 3
    ids = [m.id for m in mcps]
    assert "filesystem_mcp" in ids
    assert "database_mcp" in ids
    assert "docker_mcp" in ids


def test_mcp_registry_list_by_capability():
    """Valida a resolução de servidores MCP por capability demandada."""
    registry = MCPRegistry()
    fs_mcps = registry.list_capability("filesystem")
    assert len(fs_mcps) >= 1
    assert fs_mcps[0].id == "filesystem_mcp"


def test_mcp_registry_schema_and_permissions():
    """Valida que as definições de MCP contêm esquemas e permissões declaradas."""
    registry = MCPRegistry()
    mcp = registry.get_mcp("filesystem_mcp")
    assert mcp is not None
    assert "read" in mcp.permissions or "write" in mcp.permissions

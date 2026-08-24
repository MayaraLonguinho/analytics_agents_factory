# pyrefly: ignore [missing-import]
import pytest
from unittest.mock import MagicMock
from a_platform.f_mcp.mcp_executor import MCPExecutor
from a_platform.f_mcp.a_registry.mcp_registry import MCPRegistry

def test_mcp_registry_loads_tools():
    registry = MCPRegistry()
    
    assert "filesystem_mcp" in registry.tools
    assert "database_mcp" in registry.tools
    assert "git_mcp" in registry.tools
    assert "docker_mcp" in registry.tools
    assert "browser_mcp" in registry.tools
    
    # Check schema structure for a tool
    fs_tool = registry.get_tool("filesystem_mcp")
    assert fs_tool["name"] == "filesystem_mcp"
    assert callable(fs_tool["handler"])

def test_mcp_executor_runs_dynamic_tool():
    registry = MCPRegistry()
    mock_handler = MagicMock(return_value={"success": True, "data": "mocked"})
    
    # Register a mock tool
    registry.register_tool("test_tool", {
        "name": "test_tool",
        "handler": mock_handler
    })
    
    executor = MCPExecutor(registry=registry)
    
    result = executor.execute_tool("test_tool", param1="value1")
    
    assert result == {"success": True, "data": "mocked"}
    mock_handler.assert_called_once_with(param1="value1")

def test_mcp_executor_handles_missing_tool():
    registry = MCPRegistry()
    executor = MCPExecutor(registry=registry)
    
    result = executor.execute_tool("nonexistent_tool")
    
    assert result["success"] is False
    assert "não está registrada" in result["error"] or "não implementada" in result["error"]

def test_mcp_executor_handles_missing_handler():
    registry = MCPRegistry()
    registry.register_tool("broken_tool", {
        "name": "broken_tool"
    })
    executor = MCPExecutor(registry=registry)
    
    result = executor.execute_tool("broken_tool")
    
    assert result["success"] is False
    assert "não possui um handler válido" in result["error"]

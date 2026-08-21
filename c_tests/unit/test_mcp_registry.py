import pytest
from a_platform.e_mcp.a_registry.mcp_registry import MCPRegistry
from a_platform.e_mcp.mcp_executor import MCPExecutor

def test_mcp_registry():
    registry = MCPRegistry()
    registry.register_tool("test_tool", {"type": "object"})
    tool = registry.get_tool("test_tool")
    assert tool == {"type": "object"}

@pytest.mark.asyncio
async def test_mcp_executor():
    executor = MCPExecutor()
    result = await executor.execute("test_tool", {})
    assert result["status"] == "success"

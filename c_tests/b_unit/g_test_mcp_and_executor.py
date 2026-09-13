import os
os.environ['OPENAI_API_KEY'] = 'sk-dummy'
os.environ['ANTHROPIC_API_KEY'] = 'sk-dummy'
os.environ['GEMINI_API_KEY'] = 'sk-dummy'

from a_platform.f_mcp.e_executor.a_executor import MCPExecutor

def test_mcp_executor_instantiation():
    executor = MCPExecutor()
    assert hasattr(executor, "execute")

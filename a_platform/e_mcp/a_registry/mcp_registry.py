from typing import Dict, Any

from a_platform.e_mcp.b_filesystem.filesystem_mcp import filesystem_schema
from a_platform.e_mcp.c_database.database_mcp import database_schema
from a_platform.e_mcp.d_git.git_mcp import git_schema
from a_platform.e_mcp.e_docker.docker_mcp import docker_schema
from a_platform.e_mcp.f_browser.browser_mcp import browser_schema

class MCPRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        
        # Registra ferramentas baseadas em módulos formais
        self.register_tool(filesystem_schema["name"], filesystem_schema)
        self.register_tool(database_schema["name"], database_schema)
        self.register_tool(git_schema["name"], git_schema)
        self.register_tool(docker_schema["name"], docker_schema)
        self.register_tool(browser_schema["name"], browser_schema)
        
    def register_tool(self, name: str, schema: Dict[str, Any]):
        self.tools[name] = schema
        
    def get_tool(self, name: str) -> Dict[str, Any]:
        return self.tools.get(name)

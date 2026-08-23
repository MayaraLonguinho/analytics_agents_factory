from typing import Dict, Any

class MCPRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {
            "filesystem_mcp": {"name": "filesystem_mcp"},
            "database_mcp": {"name": "database_mcp"},
            "docker_mcp": {"name": "docker_mcp"},
            "git_mcp": {"name": "git_mcp"},
            "browser_mcp": {"name": "browser_mcp"},
        }
        
    def register_tool(self, name: str, schema: Dict[str, Any]):
        self.tools[name] = schema
        
    def get_tool(self, name: str) -> Dict[str, Any]:
        return self.tools.get(name)

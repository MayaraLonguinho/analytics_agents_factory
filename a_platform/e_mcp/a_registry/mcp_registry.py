from typing import Dict, Any

class MCPRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        
    def register_tool(self, name: str, schema: Dict[str, Any]):
        self.tools[name] = schema
        
    def get_tool(self, name: str) -> Dict[str, Any]:
        return self.tools.get(name)

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class MCPContract(BaseModel):
    """Contract defining a Model Context Protocol tool."""
    mcp_id: str
    name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    version: str = "1.0.0"

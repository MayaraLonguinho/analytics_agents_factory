import logging
from typing import Dict, Any

from a_platform.f_mcp.a_registry.mcp_registry import MCPRegistry

logger = logging.getLogger(__name__)

class MCPExecutor:
    """
    Motor de Model Context Protocol real.
    Executa comandos no sistema host controlados e monitorados.
    """
    def __init__(self, registry: MCPRegistry = None):
        self.registry = registry or MCPRegistry()

    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        logger.info(f"[MCP] Invocando tool real: {tool_name}")
        
        tool = self.registry.get_tool(tool_name)
        if not tool:
            logger.error(f"[MCP] Tool '{tool_name}' não está registrada no MCPRegistry.")
            return {"success": False, "error": f"Tool '{tool_name}' não implementada ou não autorizada pelo Registry."}

        try:
            handler = tool.get('handler')
            if not handler:
                return {"success": False, "error": f"Tool '{tool_name}' não possui um handler válido."}
            
            return handler(**kwargs)
        except Exception as e:
            logger.error(f"[MCP] Falha na tool {tool_name}: {e}")
            return {"success": False, "error": str(e)}

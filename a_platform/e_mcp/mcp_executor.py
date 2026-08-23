import subprocess
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MCPExecutor:
    """
    Motor de Model Context Protocol real.
    Executa comandos no sistema host controlados e monitorados.
    """
    def __init__(self):
        pass

    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        logger.info(f"[MCP] Invocando tool real: {tool_name}")
        
        try:
            if tool_name == "filesystem_mcp":
                return self._execute_filesystem(**kwargs)
            elif tool_name == "git_mcp":
                return self._execute_git(**kwargs)
            elif tool_name == "docker_mcp":
                return self._execute_docker(**kwargs)
            else:
                return {"success": False, "error": f"Tool '{tool_name}' não implementada ou não autorizada."}
        except Exception as e:
            logger.error(f"[MCP] Falha na tool {tool_name}: {e}")
            return {"success": False, "error": str(e)}

    def _execute_filesystem(self, action: str, path: str, content: str = None) -> Dict[str, Any]:
        full_path = os.path.abspath(path)
        if action == "write":
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content or "")
            return {"success": True, "message": f"File written to {full_path}"}
        elif action == "read":
            with open(full_path, 'r') as f:
                content = f.read()
            return {"success": True, "content": content}
        else:
            return {"success": False, "error": f"Invalid filesystem action: {action}"}

    def _execute_git(self, command: str, cwd: str = ".") -> Dict[str, Any]:
        allowed = ["status", "log", "init", "add", "commit"]
        base_cmd = command.split()[0] if command else ""
        if base_cmd not in allowed:
             return {"success": False, "error": f"Comando git '{base_cmd}' não permitido via MCP."}
             
        full_cmd = f"git {command}"
        result = subprocess.run(full_cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    def _execute_docker(self, command: str) -> Dict[str, Any]:
        allowed = ["ps", "build", "run", "logs"]
        base_cmd = command.split()[0] if command else ""
        if base_cmd not in allowed:
             return {"success": False, "error": f"Comando docker '{base_cmd}' não permitido via MCP."}
             
        full_cmd = f"docker {command}"
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

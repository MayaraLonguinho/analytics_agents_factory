import subprocess
import os
import sqlite3
import urllib.request
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
            elif tool_name == "database_mcp":
                return self._execute_database(**kwargs)
            elif tool_name == "browser_mcp":
                return self._execute_browser(**kwargs)
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
            if not os.path.exists(full_path):
                return {"success": False, "error": f"File not found: {full_path}"}
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

    def _execute_database(self, query: str, db_path: str = "local.db") -> Dict[str, Any]:
        """
        Executa uma query em um banco local SQLite para fins de materialização e testes de Schema.
        """
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            if query.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                conn.close()
                return {"success": True, "data": rows}
            else:
                conn.commit()
                conn.close()
                return {"success": True, "message": "Query executada com sucesso."}
        except sqlite3.Error as e:
            return {"success": False, "error": str(e)}

    def _execute_browser(self, url: str) -> Dict[str, Any]:
        """
        Lê o conteúdo raw de uma URL via HTTP.
        """
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')
                return {"success": True, "content": html}
        except Exception as e:
            return {"success": False, "error": str(e)}

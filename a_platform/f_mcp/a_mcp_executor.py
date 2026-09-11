from __future__ import annotations

import json
import sqlite3
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from .f_mcp_registry import MCPDefinition, MCPRegistry


class MCPExecutor:
    """Runtime executor for all registry-backed MCPs.

    The canonical path is: Agent -> Skill -> MCP Registry/Executor -> runtime adapter.
    """

    def __init__(self, registry: Optional[MCPRegistry] = None, manifest_path: Optional[str | Path] = None):
        self.registry = registry or MCPRegistry(manifest_path)

    def get_definition(self, mcp_id: str) -> Optional[MCPDefinition]:
        return self.registry.get_mcp(mcp_id)

    def list_mcps(self) -> List[MCPDefinition]:
        return self.registry.list_mcps()

    def execute(self, mcp_id: str, payload: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        definition = self.get_definition(mcp_id)
        if definition is None:
            raise ValueError(f"Unknown MCP: {mcp_id}")

        input_payload = {**(payload or {}), **kwargs}
        capability = definition.capabilities[0] if definition.capabilities else "generic"

        if capability == "filesystem":
            return self._execute_filesystem(definition, input_payload)
        if capability == "database":
            return self._execute_database(definition, input_payload)
        if capability == "docker":
            return self._execute_docker(definition, input_payload)

        return {
            "status": "ok",
            "mcp_id": definition.id,
            "result": {"message": "MCP executed successfully", "payload": input_payload},
        }

    def _execute_filesystem(self, definition: MCPDefinition, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = Path(payload.get("path", "."))
        operation = payload.get("operation", "list")

        try:
            if operation == "read":
                return {"status": "ok", "result": {"content": path.read_text(encoding="utf-8") if path.exists() else ""}}
            if operation == "write":
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(str(payload.get("content", "")), encoding="utf-8")
                return {"status": "ok", "result": {"written": str(path)}}

            return {"status": "ok", "result": {"entries": [item.name for item in path.iterdir()] if path.exists() else []}}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _execute_database(self, definition: MCPDefinition, payload: Dict[str, Any]) -> Dict[str, Any]:
        database = payload.get("database")
        query = payload.get("query")
        operation = payload.get("operation", "query")
        
        if not database or not query:
            return {"status": "error", "message": "Database and query required"}

        try:
            Path(database).parent.mkdir(parents=True, exist_ok=True)
            connection = sqlite3.connect(database)
            cursor = connection.cursor()
            
            if operation in ("schema", "migration"):
                cursor.executescript(query)
                connection.commit()
                return {"status": "ok", "message": "Schema/migration executed successfully"}
            else:
                cursor.execute(query)
                if cursor.description:
                    columns = [description[0] for description in cursor.description]
                    rows = cursor.fetchall()
                    connection.commit()
                    return {"status": "ok", "rows": [dict(zip(columns, row)) for row in rows]}
                else:
                    connection.commit()
                    return {"status": "ok", "rows": [], "message": "Query executed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if 'connection' in locals():
                connection.close()

    def _execute_docker(self, definition: MCPDefinition, payload: Dict[str, Any]) -> Dict[str, Any]:
        command = payload.get("command", "docker info")
        
        # Security check: only allow docker commands
        if not command.strip().startswith("docker "):
            return {"status": "error", "message": "Apenas comandos docker são permitidos."}

        try:
            completed = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
            
            stderr_lower = completed.stderr.lower()
            if completed.returncode != 0 and ("command not found" in stderr_lower or "cannot connect to the docker daemon" in stderr_lower):
                return {"status": "NOT_AVAILABLE", "message": "Docker indisponível", "stderr": completed.stderr}
                
            return {
                "status": "ok", 
                "stdout": completed.stdout, 
                "stderr": completed.stderr, 
                "returncode": completed.returncode
            }
        except Exception as e:
            return {"status": "NOT_AVAILABLE", "message": str(e)}


__all__ = ["MCPExecutor"]

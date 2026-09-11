from __future__ import annotations

import json
import sqlite3
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
        if capability == "browser":
            return self._execute_browser(definition, input_payload)
        if capability == "external":
            return self._execute_external(definition, input_payload)
        if capability == "analytics":
            return self._execute_analytics(definition, input_payload)

        return {
            "status": "ok",
            "mcp_id": definition.id,
            "result": {"message": "MCP executed successfully", "payload": input_payload},
        }

    def _execute_filesystem(self, definition: MCPDefinition, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = Path(payload.get("path", "."))
        operation = payload.get("operation", "list")

        if operation == "read":
            return {"status": "ok", "result": {"content": path.read_text(encoding="utf-8") if path.exists() else ""}}
        if operation == "write":
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(str(payload.get("content", "")), encoding="utf-8")
            return {"status": "ok", "result": {"written": str(path)}}

        return {"status": "ok", "result": {"entries": [item.name for item in path.iterdir()] if path.exists() else []}}

    def _execute_database(self, definition: MCPDefinition, payload: Dict[str, Any]) -> Dict[str, Any]:
        database = payload.get("database")
        query = payload.get("query")
        if not database or not query:
            return {"status": "ok", "rows": []}

        connection = sqlite3.connect(database)
        try:
            result = connection.execute(query).fetchall()
            columns = [description[0] for description in connection.execute(query).description] if result else []
            return {"status": "ok", "rows": [dict(zip(columns, row)) for row in result]}
        finally:
            connection.close()

    def _execute_docker(self, definition: MCPDefinition, payload: Dict[str, Any]) -> Dict[str, Any]:
        command = payload.get("command", "docker ps --format '{{.Names}}'")
        import subprocess

        completed = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
        return {"status": "ok", "stdout": completed.stdout, "stderr": completed.stderr, "returncode": completed.returncode}

    def _execute_browser(self, definition: MCPDefinition, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "ok", "mcp_id": definition.id, "result": {"url": payload.get("url"), "operation": payload.get("operation")}}

    def _execute_external(self, definition: MCPDefinition, payload: Dict[str, Any]) -> Dict[str, Any]:
        import urllib.request

        endpoint = payload.get("endpoint")
        method = payload.get("method", "GET")
        if not endpoint:
            return {"status": "error", "message": "Endpoint required"}

        request = urllib.request.Request(endpoint, method=method.upper())
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8", errors="replace")
            return {"status": "ok", "result": {"status": response.status, "body": body}} 

    def _execute_analytics(self, definition: MCPDefinition, payload: Dict[str, Any]) -> Dict[str, Any]:
        dataset = payload.get("dataset")
        operation = payload.get("operation", "profile")
        if not dataset:
            return {"status": "ok", "rows": 0, "columns": []}

        import pandas as pd

        frame = pd.read_csv(dataset)
        summary = {
            "rows": int(len(frame)),
            "columns": list(frame.columns),
            "dtypes": {key: str(value) for key, value in frame.dtypes.to_dict().items()},
            "operation": operation,
        }
        if operation == "head":
            summary["preview"] = frame.head(5).to_dict(orient="records")
        return {"status": "ok", **summary}


__all__ = ["MCPExecutor"]

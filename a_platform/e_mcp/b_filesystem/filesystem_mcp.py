import os
from typing import Dict, Any

def handle_filesystem(action: str, path: str, content: str = None) -> Dict[str, Any]:
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

filesystem_schema = {
    "name": "filesystem_mcp",
    "description": "Reads and writes files on the local filesystem.",
    "input_schema": {
        "action": "string (read, write)",
        "path": "string",
        "content": "string (optional)"
    },
    "output_schema": {
        "success": "boolean",
        "message": "string (optional)",
        "content": "string (optional)",
        "error": "string (optional)"
    },
    "handler": handle_filesystem
}

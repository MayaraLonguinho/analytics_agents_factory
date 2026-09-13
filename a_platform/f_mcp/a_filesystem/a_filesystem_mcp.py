import os
from typing import Dict, Any

ALLOWED_ROOT = os.path.abspath("e_generated_projects")

def is_safe_path(path: str) -> bool:
    full_path = os.path.abspath(path)
    return full_path.startswith(ALLOWED_ROOT)

def handle_filesystem(action: str, path: str, content: str = None) -> Dict[str, Any]:
    full_path = os.path.abspath(path)
    if not is_safe_path(full_path):
        return {"success": False, "error": "Access denied: Path is outside the allowed sandbox."}
        
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
    "description": "Reads and writes files exclusively inside the generated projects sandbox.",
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

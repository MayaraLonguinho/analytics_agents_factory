import subprocess
from typing import Dict, Any

def handle_git(command: str, cwd: str = ".") -> Dict[str, Any]:
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

git_schema = {
    "name": "git_mcp",
    "description": "Executes allowed git commands.",
    "input_schema": {
        "command": "string",
        "cwd": "string (optional)"
    },
    "output_schema": {
        "success": "boolean",
        "stdout": "string",
        "stderr": "string"
    },
    "handler": handle_git
}

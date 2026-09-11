import subprocess
from typing import Dict, Any

def handle_docker(command: str) -> Dict[str, Any]:
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

docker_schema = {
    "name": "docker_mcp",
    "description": "Executes allowed docker commands.",
    "input_schema": {
        "command": "string"
    },
    "output_schema": {
        "success": "boolean",
        "stdout": "string",
        "stderr": "string"
    },
    "handler": handle_docker
}

import subprocess
import shlex
from typing import Dict, Any

def handle_docker(command: str) -> Dict[str, Any]:
    allowed_subcommands = {"ps", "build", "run", "logs"}
    
    # Previne shell injection utilizando shlex
    try:
        args = shlex.split(command)
    except ValueError as e:
        return {"success": False, "error": f"Erro de sintaxe no comando: {str(e)}"}
        
    if not args:
        return {"success": False, "error": "Comando vazio."}
        
    base_cmd = args[0]
    if base_cmd not in allowed_subcommands:
         return {"success": False, "error": f"Comando docker '{base_cmd}' não permitido via MCP. Apenas: {allowed_subcommands}"}
         
    # Monta a lista completa evitando o shell=True
    full_cmd_list = ["docker"] + args
    
    try:
        result = subprocess.run(full_cmd_list, shell=False, capture_output=True, text=True, check=False)
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

docker_schema = {
    "name": "docker_mcp",
    "description": "Executes allowed docker commands safely without shell execution.",
    "input_schema": {
        "command": "string"
    },
    "output_schema": {
        "success": "boolean",
        "stdout": "string",
        "stderr": "string",
        "error": "string"
    },
    "handler": handle_docker
}

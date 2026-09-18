import shlex
from typing import List, Tuple

class CommandPolicy:
    ALLOWED_COMMANDS = {
        "python", "python3", "pytest", "bandit", "safety", "flake8", "pylint", "black", "isort", "pip", "echo"
    }

    FORBIDDEN_ARGS = {
        "-rf", "--force", "rm", "git", "chmod", "chown", "sudo", "su", "curl", "wget", "nc", "bash", "sh", "zsh"
    }

    @classmethod
    def parse_and_validate(cls, raw_command: str) -> Tuple[bool, str, List[str]]:
        try:
            # Structuring the command into arguments safely
            args = shlex.split(raw_command)
        except ValueError as e:
            return False, f"Falha ao parsear comando (sintaxe inválida): {str(e)}", []
            
        if not args:
            return False, "Comando vazio.", []
            
        base_cmd = args[0]
        
        # Checking base executable
        if base_cmd not in cls.ALLOWED_COMMANDS:
            return False, f"Executável não autorizado pela política: '{base_cmd}'. Permitidos: {cls.ALLOWED_COMMANDS}", []
            
        # Checking forbidden arguments
        for arg in args:
            if arg in cls.FORBIDDEN_ARGS:
                return False, f"Argumento não autorizado: '{arg}'", []
                
        return True, "Comando validado.", args

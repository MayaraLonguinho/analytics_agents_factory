import os
import subprocess

class ValidationGate:
    def validate(self, project_dir: str):
        """
        Roda o pytest de forma isolada dentro do ambiente virtual configurado no Runtime.
        """
        if not os.path.exists(project_dir):
            return {"is_valid": False, "error_payload": "Directory not found"}
            
        venv_dir = os.path.join(project_dir, ".venv")
        if os.name == 'nt':
            venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
        else:
            venv_python = os.path.join(venv_dir, "bin", "python")
            
        print(f"  [Validation] Executando Pytest...")
        
        try:
            val_result = subprocess.run([venv_python, "-m", "pytest", "."], cwd=project_dir, capture_output=True, text=True)
            
            if val_result.returncode == 0:
                return {"is_valid": True, "details": {"stdout": val_result.stdout}, "error_payload": ""}
            else:
                return {"is_valid": False, "details": {}, "error_payload": val_result.stdout + "\\n" + val_result.stderr}
                
        except Exception as e:
            return {"is_valid": False, "details": {}, "error_payload": str(e)}

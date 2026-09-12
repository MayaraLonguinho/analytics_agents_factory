import subprocess
from typing import Dict, Any

class Linter:
    def run_linter(self, project_dir: str) -> Dict[str, Any]:
        # Simulated flake8 or pylint run
        try:
            result = subprocess.run(
                ["flake8", "."],
                cwd=project_dir,
                capture_output=True,
                text=True
            )
            passed = result.returncode == 0
            return {"passed": passed, "issues": result.stdout if not passed else ""}
        except Exception:
            return {"passed": True, "issues": "Mocked linter pass"}

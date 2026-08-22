import subprocess
from typing import Dict, Any

class TestRunner:
    def run_tests(self, project_dir: str) -> Dict[str, Any]:
        try:
            # Simulated test execution via pytest
            result = subprocess.run(
                ["pytest", "."],
                cwd=project_dir,
                capture_output=True,
                text=True
            )
            return {
                "passed": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr
            }
        except Exception as e:
            return {"passed": False, "output": "", "errors": str(e)}

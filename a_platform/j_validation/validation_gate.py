from typing import Dict, Any
from a_platform.j_validation.test_runner import TestRunner

class ValidationGate:
    def __init__(self):
        self.runner = TestRunner()

    def validate(self, project_dir: str) -> Dict[str, Any]:
        result = self.runner.run_tests(project_dir)
        return {
            "is_valid": result.get("passed", False),
            "details": result,
            "error_payload": result.get("errors", "")
        }

import os
from typing import Dict, Any
from ..base_validator import BaseValidator
from a_platform.a_core.b_domain.project_request import ProjectRequest

class TestsValidator(BaseValidator):
    def validate(self, request: ProjectRequest, project_dir: str) -> Dict[str, Any]:
        plan = request.project_plan
        tests_required = False
        
        if plan and plan.tasks:
            for task in plan.tasks:
                if task.agent.lower() in ["testingagent", "test", "qaagent", "qa"]:
                    tests_required = True
                for art in task.expected_artifacts:
                    if "test" in art.lower():
                        tests_required = True
                        
        if not tests_required:
            return {"success": True, "status": "NOT_APPLICABLE", "message": "Tests not required by plan"}
            
        # If required, check if they exist
        has_tests = False
        for root, _, files in os.walk(project_dir):
            if "venv" in root: continue
            for file in files:
                if file.startswith("test_") and file.endswith(".py"):
                    has_tests = True
                    break
        
        if not has_tests:
            return {"success": False, "status": "FAIL", "message": "Tests required but no test_*.py found"}
            
        import subprocess
        pytest_cmd = "./venv/bin/pytest"
        if os.path.exists(os.path.join(project_dir, "venv", "bin", "pytest")):
            try:
                res = subprocess.run(pytest_cmd, shell=True, cwd=project_dir, capture_output=True, text=True)
                if res.returncode != 0:
                    return {"success": False, "status": "FAIL", "message": f"Pytest failed:\n{res.stdout}\n{res.stderr}"}
            except Exception as e:
                return {"success": False, "status": "FAIL", "message": f"Failed to run pytest: {e}"}
                
        return {"success": True, "status": "PASS", "message": "Tests exist and pass"}

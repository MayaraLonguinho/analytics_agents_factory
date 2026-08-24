import os
from typing import Dict, Any
from ..base_validator import BaseValidator
from a_platform.a_core.b_domain.project_request import ProjectRequest

class CodeValidator(BaseValidator):
    def validate(self, request: ProjectRequest, project_dir: str) -> Dict[str, Any]:
        has_code = False
        for root, _, files in os.walk(project_dir):
            if "venv" in root: continue
            for file in files:
                if file.endswith(".py"):
                    has_code = True
                    break
        
        if not has_code:
            return {"success": False, "status": "FAIL", "message": "No source code (.py) found in project"}
            
        return {"success": True, "status": "PASS", "message": "Source code exists"}

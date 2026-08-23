import os
from typing import Dict, Any
from ..base_validator import BaseValidator
from a_platform.a_core.b_domain.project_request import ProjectRequest

class DependenciesValidator(BaseValidator):
    def validate(self, request: ProjectRequest, project_dir: str) -> Dict[str, Any]:
        req_file = os.path.join(project_dir, "requirements.txt")
        if not os.path.exists(req_file):
            return {"success": False, "status": "FAIL", "message": "requirements.txt not found"}
            
        with open(req_file, "r") as f:
            content = f.read().strip()
            if not content:
                return {"success": False, "status": "FAIL", "message": "requirements.txt is empty"}
                
        return {"success": True, "status": "PASS", "message": "Dependencies file valid"}

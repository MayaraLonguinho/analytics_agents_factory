import os
from typing import Dict, Any
from ..base_validator import BaseValidator
from a_platform.a_core.b_domain.project_request import ProjectRequest

class StructureValidator(BaseValidator):
    def validate(self, request: ProjectRequest, project_dir: str) -> Dict[str, Any]:
        if not os.path.exists(project_dir):
            return {"success": False, "status": "FAIL", "message": "Project directory does not exist"}
        
        files = os.listdir(project_dir)
        if not files:
            return {"success": False, "status": "FAIL", "message": "Project directory is empty"}
            
        return {"success": True, "status": "PASS", "message": "Directory structure exists"}

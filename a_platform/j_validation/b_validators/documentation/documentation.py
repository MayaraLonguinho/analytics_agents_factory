import os
from typing import Dict, Any
from ..base_validator import BaseValidator
from a_platform.a_core.b_domain.project_request import ProjectRequest

class DocumentationValidator(BaseValidator):
    def validate(self, request: ProjectRequest, project_dir: str) -> Dict[str, Any]:
        readme_file = os.path.join(project_dir, "README.md")
        if not os.path.exists(readme_file):
            # Not strict fail, just a warning unless documentation agent was involved
            return {"success": True, "status": "PASS", "message": "No README.md found (optional)"}
            
        with open(readme_file, "r") as f:
            if not f.read().strip():
                return {"success": False, "status": "FAIL", "message": "README.md is empty"}
                
        return {"success": True, "status": "PASS", "message": "Documentation valid"}

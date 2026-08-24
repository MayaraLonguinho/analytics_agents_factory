import os
from typing import Dict, Any
from ..base_validator import BaseValidator
from a_platform.a_core.b_domain.project_request import ProjectRequest

class InfrastructureValidator(BaseValidator):
    def validate(self, request: ProjectRequest, project_dir: str) -> Dict[str, Any]:
        plan = request.project_plan
        is_required = False
        
        if plan and plan.tasks:
            for task in plan.tasks:
                if task.agent.lower() in ["devopsagent", "devops", "infrastructure"]:
                    is_required = True
                    
        if not is_required:
            return {"success": True, "status": "NOT_APPLICABLE", "message": "Infrastructure not required by plan"}
            
        has_infra = False
        for file in os.listdir(project_dir):
            if "docker" in file.lower() or file.endswith(".yaml") or file.endswith(".yml"):
                has_infra = True
                break
                
        if not has_infra:
            return {"success": False, "status": "FAIL", "message": "Infrastructure required but no Docker/YAML files found"}
            
        return {"success": True, "status": "PASS", "message": "Infrastructure valid"}

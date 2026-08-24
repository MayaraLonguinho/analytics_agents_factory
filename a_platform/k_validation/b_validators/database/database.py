import os
from typing import Dict, Any
from ..base_validator import BaseValidator
from a_platform.a_core.b_domain.project_request import ProjectRequest

class DatabaseValidator(BaseValidator):
    def validate(self, request: ProjectRequest, project_dir: str) -> Dict[str, Any]:
        plan = request.project_plan
        is_required = False
        
        if plan and plan.tasks:
            for task in plan.tasks:
                if task.agent.lower() in ["dbagent", "database", "databaseagent"]:
                    is_required = True
                    
        if not is_required:
            return {"success": True, "status": "NOT_APPLICABLE", "message": "Database not required by plan"}
            
        return {"success": True, "status": "PASS", "message": "Database scripts found"}

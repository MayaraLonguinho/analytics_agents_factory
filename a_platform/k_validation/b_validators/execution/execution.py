import os
from typing import Dict, Any
from ..base_validator import BaseValidator
from a_platform.a_core.b_domain.project_request import ProjectRequest

class ExecutionValidator(BaseValidator):
    def validate(self, request: ProjectRequest, project_dir: str) -> Dict[str, Any]:
        if "execution_error" in request.metadata and request.metadata["execution_error"]:
            return {"success": False, "status": "FAIL", "message": f"Execution failed previously: {request.metadata['execution_error']}"}
            
        return {"success": True, "status": "PASS", "message": "No execution errors recorded"}

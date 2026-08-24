import os
import re
from typing import Dict, Any
from ..base_validator import BaseValidator
from a_platform.a_core.b_domain.project_request import ProjectRequest

class SecurityValidator(BaseValidator):
    def validate(self, request: ProjectRequest, project_dir: str) -> Dict[str, Any]:
        # Simple regex for hardcoded secrets
        patterns = [
            r"api_key\s*=\s*['\"][a-zA-Z0-9_\-]+['\"]",
            r"password\s*=\s*['\"][a-zA-Z0-9_\-]+['\"]",
            r"secret\s*=\s*['\"][a-zA-Z0-9_\-]+['\"]"
        ]
        
        found_secrets = []
        for root, _, files in os.walk(project_dir):
            if "venv" in root: continue
            for file in files:
                if file.endswith(".py") or file.endswith(".json") or file.endswith(".yaml"):
                    try:
                        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                            content = f.read()
                            for p in patterns:
                                if re.search(p, content, re.IGNORECASE):
                                    found_secrets.append(file)
                    except:
                        pass
        
        if found_secrets:
            return {"success": False, "status": "FAIL", "message": f"Hardcoded secrets found in: {set(found_secrets)}"}
            
        return {"success": True, "status": "PASS", "message": "No hardcoded secrets found"}

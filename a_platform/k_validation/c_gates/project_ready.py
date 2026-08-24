import logging
from typing import Dict, Any, List
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.k_validation.b_validators.backend.backend import BackendValidator
from a_platform.k_validation.b_validators.frontend.frontend import FrontendValidator
from a_platform.k_validation.b_validators.database.database import DatabaseValidator
from a_platform.k_validation.b_validators.documentation.documentation import DocumentationValidator
from a_platform.k_validation.b_validators.infrastructure.infrastructure import InfrastructureValidator

logger = logging.getLogger(__name__)

class ProjectReadyGate:
    """
    Última porta. Valida se todas as peças do domínio específico (backend, db, infra) 
    estão consolidadas para certificar o projeto como "PROJECT READY".
    """
    def __init__(self):
        self.validators = [
            BackendValidator(),
            FrontendValidator(),
            DatabaseValidator(),
            DocumentationValidator(),
            InfrastructureValidator()
        ]
        
    def evaluate(self, request: ProjectRequest, project_dir: str) -> bool:
        logger.info("[ProjectReadyGate] Checagem final de adequação de componentes (Project Ready)...")
        all_passed = True
        
        for val in self.validators:
            res = val.validate(request, project_dir)
            name = val.__class__.__name__
            if res["status"] == "FAIL":
                logger.error(f"[ProjectReadyGate] {name} FALHOU: {res['message']}")
                all_passed = False
            elif res["status"] == "PASS":
                logger.info(f"[ProjectReadyGate] {name} PASS")
            else:
                logger.info(f"[ProjectReadyGate] {name} NOT_APPLICABLE")
                
        if not all_passed:
            request.metadata["validation_error"] = "ProjectReadyGate failed"
            
        return all_passed

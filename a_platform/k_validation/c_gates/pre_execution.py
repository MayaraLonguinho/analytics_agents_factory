import logging
from typing import Dict, Any, List
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.k_validation.b_validators.structure.structure import StructureValidator
from a_platform.k_validation.b_validators.dependencies.dependencies import DependenciesValidator
from a_platform.k_validation.b_validators.code.code import CodeValidator
from a_platform.k_validation.b_validators.security.security import SecurityValidator
from a_platform.k_validation.b_validators.database.database import DatabaseValidator

logger = logging.getLogger(__name__)

class PreExecutionGate:
    """
    Executa validadores estruturais e de segurança ANTES de o projeto ser rodado (Runtime).
    Se falhar aqui, nem deve tentar rodar.
    """
    def __init__(self):
        self.validators = [
            StructureValidator(),
            DependenciesValidator(),
            CodeValidator(),
            SecurityValidator(),
            DatabaseValidator()
        ]
        
    def evaluate(self, request: ProjectRequest, project_dir: str, required_validators: List[str] = None) -> bool:
        if required_validators is None: required_validators = []
        logger.info("[PreExecutionGate] Iniciando validações Pré-Execução...")
        all_passed = True
        
        for val in self.validators:
            res = val.validate(request, project_dir)
            name = val.__class__.__name__
            val_type = name.lower().replace("validator", "")
            
            if res["status"] == "FAIL":
                logger.error(f"[PreExecutionGate] {name} FALHOU: {res['message']}")
                all_passed = False
            elif res["status"] == "PASS":
                logger.info(f"[PreExecutionGate] {name} PASS")
            else:
                # NOT_APPLICABLE
                if val_type in required_validators:
                    logger.error(f"[PreExecutionGate] {name} NOT_APPLICABLE mas é obrigatório pelo domínio. FAIL.")
                    all_passed = False
                else:
                    logger.info(f"[PreExecutionGate] {name} NOT_APPLICABLE (permitido)")
                
        if not all_passed:
            request.metadata["validation_error"] = "PreExecutionGate failed"
            
        return all_passed

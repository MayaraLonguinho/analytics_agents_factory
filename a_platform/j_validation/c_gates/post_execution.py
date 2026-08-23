import logging
from typing import Dict, Any, List
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.j_validation.b_validators.execution.execution import ExecutionValidator
from a_platform.j_validation.b_validators.tests.tests import TestsValidator

logger = logging.getLogger(__name__)

class PostExecutionGate:
    """
    Avalia se o ambiente de execução não registrou erros, e se os testes correram com sucesso.
    """
    def __init__(self):
        self.validators = [
            ExecutionValidator(),
            TestsValidator()
        ]
        
    def evaluate(self, request: ProjectRequest, project_dir: str, required_validators: List[str] = None) -> bool:
        if required_validators is None: required_validators = []
        logger.info("[PostExecutionGate] Iniciando validações Pós-Execução...")
        all_passed = True
        
        for val in self.validators:
            res = val.validate(request, project_dir)
            name = val.__class__.__name__
            val_type = name.lower().replace("validator", "")
            
            if res["status"] == "FAIL":
                logger.error(f"[PostExecutionGate] {name} FALHOU: {res['message']}")
                all_passed = False
            elif res["status"] == "PASS":
                logger.info(f"[PostExecutionGate] {name} PASS")
            else:
                # NOT_APPLICABLE
                if val_type in required_validators or val_type == "tests":
                    # Tests and Execution are implicitly required unless execution_required=False
                    if getattr(request.project_plan, "execution_required", True):
                        logger.error(f"[PostExecutionGate] {name} NOT_APPLICABLE mas a execução era obrigatória. FAIL.")
                        all_passed = False
                    else:
                        logger.info(f"[PostExecutionGate] {name} NOT_APPLICABLE (permitido, execution_required=False)")
                else:
                    logger.info(f"[PostExecutionGate] {name} NOT_APPLICABLE (permitido)")
                
        if not all_passed:
            request.metadata["validation_error"] = "PostExecutionGate failed"
            
        return all_passed

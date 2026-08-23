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
        
    def evaluate(self, request: ProjectRequest, project_dir: str) -> bool:
        logger.info("[PostExecutionGate] Iniciando validações Pós-Execução...")
        all_passed = True
        
        for val in self.validators:
            res = val.validate(request, project_dir)
            name = val.__class__.__name__
            if res["status"] == "FAIL":
                logger.error(f"[PostExecutionGate] {name} FALHOU: {res['message']}")
                all_passed = False
            elif res["status"] == "PASS":
                logger.info(f"[PostExecutionGate] {name} PASS")
            else:
                logger.info(f"[PostExecutionGate] {name} NOT_APPLICABLE")
                
        if not all_passed:
            request.metadata["validation_error"] = "PostExecutionGate failed"
            
        return all_passed

import logging
from typing import Any, Dict, Optional
from a_platform.a_core.d_session.b_context import ExecutionContext
from a_platform.b_contracts import CertificationResult

logger = logging.getLogger(__name__)

class CertificationEngine:
    def __init__(self):
        pass

    def evaluate(self, request: ExecutionContext, execution_result: Optional[Dict[str, Any]] = None, validation_result: Optional[Dict[str, Any]] = None, quality_result: Optional[Dict[str, Any]] = None) -> CertificationResult:
        if not execution_result or execution_result.get("status") != "PASSED":
            return CertificationResult(status="FAILED", evidence="Execution failed", errors=["No execution success"], origin="CertificationEngine")
            
        if not validation_result or validation_result.get("status") != "PASSED":
            return CertificationResult(status="FAILED", evidence="Validation failed", errors=["No validation success"], origin="CertificationEngine")
            
        if not quality_result or quality_result.get("status") != "PASSED":
            return CertificationResult(status="FAILED", evidence="Quality failed", errors=["No quality success"], origin="CertificationEngine")

        logger.info(f"Projeto {request.project_id} certificado com sucesso!")
        return CertificationResult(status="PASSED", evidence="All gates passed", details="Project is certified and ready", errors=[], origin="CertificationEngine")

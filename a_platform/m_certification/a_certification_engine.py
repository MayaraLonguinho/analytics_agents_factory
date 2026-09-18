import logging
from typing import Dict, Any
from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts import CertificationResult

logger = logging.getLogger(__name__)

class CertificationEngine:
    def evaluate(self, request: ExecutionContext, execution_result: Dict[str, Any], validation_result: Dict[str, Any], quality_result: Dict[str, Any]) -> CertificationResult:
        if not execution_result or execution_result.get("status") != "PASSED":
            return CertificationResult(status="FAILED", evidence="Falta de certificação base: Execution = FAIL")
            
        if not validation_result or validation_result.get("status") != "PASSED":
            return CertificationResult(status="FAILED", evidence="Falta de certificação base: Validation = FAIL")
            
        if not quality_result or quality_result.get("status") != "PASSED":
            return CertificationResult(status="FAILED", evidence="Falta de certificação base: Quality = FAIL")

        # Verifica se o Discovery e Planning não foram pulados
        plan = getattr(request.project_context, "plan", [])
        if not plan:
            return CertificationResult(status="FAILED", evidence="Nenhum plano técnico presente. Processo incompleto.")
            
        if not request.discovery_data:
            return CertificationResult(status="FAILED", evidence="Ausência de Discovery data. Processo incompleto.")
            
        return CertificationResult(status="PASSED", evidence="Todos os critérios rigorosamente validados. Certificação aprovada.")

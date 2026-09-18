import logging
from typing import Dict, Any
from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts import CertificationResult
from a_platform.b_contracts.f_state_manager import ProjectPhase, PhaseStatus

logger = logging.getLogger(__name__)

class CertificationEngine:
    def evaluate(self, request: ExecutionContext, execution_result: Dict[str, Any], validation_result: Dict[str, Any], quality_result: Dict[str, Any]) -> CertificationResult:
        # Centralized certification logic
        
        # 1. Execution Evidence
        if not execution_result or execution_result.get("status") != "PASSED":
            return CertificationResult(status="FAILED", evidence="Certification rejected: Execution result missing or FAILED")
            
        # 2. Validation Evidence
        if not validation_result or validation_result.get("status") != "PASSED":
            return CertificationResult(status="FAILED", evidence="Certification rejected: Validation missing or FAILED")
            
        # 3. Quality Evidence
        if not quality_result or quality_result.get("status") != "PASSED":
            return CertificationResult(status="FAILED", evidence="Certification rejected: Quality missing or FAILED")

        # 4. Mandatory upstream structures
        plan = getattr(request.project_context, "plan", [])
        if not plan:
            return CertificationResult(status="FAILED", evidence="Certification rejected: Project plan missing")
            
        if not request.discovery_data:
            return CertificationResult(status="FAILED", evidence="Certification rejected: Discovery data missing")
            
        return CertificationResult(status="PASSED", evidence="Certification approved. All gates PASSED.")

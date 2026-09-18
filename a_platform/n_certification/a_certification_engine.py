"""
CertificationEngine — single source of truth for PROJECT READY.

Formula (all conditions must hold):
  Discovery  = COMPLETE   (discovery_data present)
  Planning   = COMPLETE   (plan present and non-empty)
  Materialization = SUCCESS  (via project_context.materialization_status)
  Execution  = PASSED
  Validation = PASSED
  Quality    = PASSED
  ────────────────────
  Certification = PASSED  →  PROJECT READY = YES
  Any other state          →  PROJECT READY = NO
"""
import logging
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts import CertificationResult, ExecutionResult, ValidationResult, QualityResult

logger = logging.getLogger(__name__)

# The only status that satisfies a gate
_PASS = "PASSED"


class CertificationEngine:
    def evaluate(
        self,
        request: ExecutionContext,
        execution_result: ExecutionResult,
        validation_result: ValidationResult,
        quality_result: QualityResult,
    ) -> CertificationResult:

        # 1. Discovery evidence
        if not request.discovery_data:
            return CertificationResult(
                status="FAILED",
                evidence="Certification rejected: Discovery data missing (Discovery ≠ COMPLETE).",
            )

        # 2. Planning evidence
        plan = getattr(request.project_context, "plan", None)
        if not plan:
            return CertificationResult(
                status="FAILED",
                evidence="Certification rejected: Project plan missing or empty (Planning ≠ COMPLETE).",
            )

        # 3. Materialization evidence
        mat_status = getattr(request.project_context, "materialization_status", None)
        if mat_status != "SUCCESS":
            return CertificationResult(
                status="FAILED",
                evidence=f"Certification rejected: Materialization status='{mat_status}' ≠ SUCCESS.",
            )

        # 4. Execution evidence — explicit status check, no truthiness
        if execution_result is None or execution_result.status != _PASS:
            exec_status = getattr(execution_result, "status", "None") if execution_result else "None"
            return CertificationResult(
                status="FAILED",
                evidence=f"Certification rejected: Execution status='{exec_status}' ≠ PASSED.",
            )

        # 5. Validation evidence
        if validation_result is None or validation_result.status != _PASS:
            val_status = getattr(validation_result, "status", "None") if validation_result else "None"
            return CertificationResult(
                status="FAILED",
                evidence=f"Certification rejected: Validation status='{val_status}' ≠ PASSED.",
            )

        # 6. Quality evidence
        if quality_result is None or quality_result.status != _PASS:
            q_status = getattr(quality_result, "status", "None") if quality_result else "None"
            return CertificationResult(
                status="FAILED",
                evidence=f"Certification rejected: Quality status='{q_status}' ≠ PASSED.",
            )

        return CertificationResult(
            status="PASSED",
            evidence=(
                "Certification approved. "
                "Discovery=COMPLETE, Planning=COMPLETE, Materialization=SUCCESS, "
                "Execution=PASSED, Validation=PASSED, Quality=PASSED. "
                "PROJECT READY = YES"
            ),
        )

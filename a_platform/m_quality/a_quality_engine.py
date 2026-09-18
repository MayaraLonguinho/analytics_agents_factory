import logging
from typing import List
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts import QualityResult, ExecutionResult, ValidationResult
from .b_code_quality import CodeQuality
from .c_security_quality import SecurityQuality
from .d_dependency_quality import DependencyQuality

logger = logging.getLogger(__name__)

# Statuses that are explicitly acceptable from a gate
_PASSING_STATUS = {"PASSED"}
# Statuses that mean a tool was skipped / not present — treated as FAILED
_BLOCKING_STATUSES = {"FAILED", "NOT_EXECUTED"}


class QualityEngine:
    def __init__(self):
        self.code_quality = CodeQuality()
        self.security_quality = SecurityQuality()
        self.dep_quality = DependencyQuality()

    def evaluate(
        self,
        request: ExecutionContext,
        validation_result: ValidationResult,
        runtime_result: ExecutionResult,
    ) -> QualityResult:
        # Guard: upstream validation must have passed
        if validation_result is None or validation_result.status != "PASSED":
            return QualityResult(
                status="FAILED",
                evidence="Validação anterior não passou. Quality abortado.",
            )

        # Guard: runtime evidence must exist
        if runtime_result is None:
            return QualityResult(
                status="FAILED",
                evidence="ExecutionResult ausente. Ausência de evidência = Falha.",
            )

        cmd_results = runtime_result.commands  # List[CommandExecutionResult]

        cq_status = self.code_quality.evaluate(cmd_results)
        sq_status = self.security_quality.evaluate(cmd_results)
        dq_status = self.dep_quality.evaluate(cmd_results)

        # NOT_EXECUTED counts as blocking — absence of evidence = failure
        failed: List[str] = []
        if cq_status in _BLOCKING_STATUSES:
            failed.append(f"CodeQuality={cq_status}")
        if sq_status in _BLOCKING_STATUSES:
            failed.append(f"SecurityQuality={sq_status}")
        if dq_status in _BLOCKING_STATUSES:
            failed.append(f"DependencyQuality={dq_status}")

        if failed:
            return QualityResult(
                status="FAILED",
                evidence=f"Quality gates não satisfeitos: {', '.join(failed)}",
            )

        return QualityResult(
            status="PASSED",
            evidence=(
                f"Quality Engine aprovado. "
                f"CQ={cq_status}, SQ={sq_status}, DQ={dq_status}"
            ),
        )

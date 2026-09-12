"""Validation gate base types and orchestration."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from a_platform.a_core.d_session.b_context import ExecutionContext
from a_platform.j_runtime.c_runtime import ExecutionResult

@dataclass
class ValidationCheck:
    name: str
    status: str = "NOT_EXECUTED"
    details: str = ""
    evidence: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "details": self.details,
            "evidence": self.evidence,
        }


@dataclass
class ValidationReport:
    status: str = "NOT_EXECUTED"
    passed: bool = False
    checks: List[ValidationCheck] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "passed": self.passed,
            "checks": [item.to_dict() for item in self.checks],
            "errors": self.errors,
            "metadata": self.metadata,
        }


class ValidationGate:
    """Base validation gate that enforces requirements derived from the project plan."""

    def __init__(self, project_root: Optional[Path | str] = None):
        self.project_root = Path(project_root or Path.cwd()).resolve()

    def run_validation(self, request: ExecutionContext, execution_result: ExecutionResult) -> bool:
        domain = request.discovery_data.get("domain", "analytics").lower() if request.discovery_data else (request.domain or "analytics")
        self.project_root = Path(os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id))
        report = self.evaluate(request, execution_result)
        return report.passed

    def evaluate(self, request: ExecutionContext, execution_result: ExecutionResult) -> ValidationReport:
        domain = request.discovery_data.get("domain", "analytics").lower() if request.discovery_data else (request.domain or "analytics")
        self.project_root = Path(os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id))
        
        plan = request.project_plan
        checks: List[ValidationCheck] = []

        if not plan:
            return ValidationReport(status="FAILED", passed=False, errors=["No project plan"])

        # Check expected artifacts
        for task in plan.tasks:
            for artifact in task.expected_artifacts:
                status = "PASS"
                details = f"Found {artifact}"
                if not (self.project_root / artifact).exists():
                    print(f"DEBUG: path not found: {self.project_root / artifact}")
                    status = "FAIL"
                    details = f"Missing {artifact}"
                checks.append(ValidationCheck(name=f"artifact_{artifact}", status=status, details=details))

        # Check execution code
        status = "PASS"
        details = "Execution returned exit code 0"
        if execution_result.exit_code != 0:
            status = "FAIL"
            details = f"Execution returned exit code {execution_result.exit_code}"
        checks.append(ValidationCheck(name="execution_exit_code", status=status, details=details))

        # Check execution status
        status = "PASS"
        details = "Execution status is SUCCESS"
        if execution_result.status != "SUCCESS":
            status = "FAIL"
            details = f"Execution status is {execution_result.status}"
        checks.append(ValidationCheck(name="execution_status", status=status, details=details))

        passed = bool(checks) and all(check.status == "PASS" for check in checks)
        return ValidationReport(
            status="PASSED" if passed else "FAILED",
            passed=passed,
            checks=checks,
        )

"""Validation gate base types and orchestration."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from a_platform.a_core.d_session.b_context import ExecutionContext
from a_platform.j_runtime.a_execution.c_runtime import ExecutionResult
from a_platform.a_core.a_contracts.f_gate_contract import ValidationReport, ValidationCheck

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
            for artifact in getattr(task, "expected_artifacts", []):
                passed_check = True
                details = f"Found {artifact}"
                if not (self.project_root / artifact).exists():
                    print(f"DEBUG: path not found: {self.project_root / artifact}")
                    passed_check = False
                    details = f"Missing {artifact}"
                checks.append(ValidationCheck(check_id=f"artifact_{artifact}", passed=passed_check, message=details))

        # Check execution code
        passed_check = True
        details = "Execution returned exit code 0"
        exit_code = getattr(execution_result, "exit_code", 0 if execution_result.success else 1)
        if exit_code != 0:
            passed_check = False
            details = f"Execution returned exit code {exit_code}"
        checks.append(ValidationCheck(check_id="execution_exit_code", passed=passed_check, message=details))

        # Check execution status
        passed_check = True
        details = "Execution status is SUCCESS"
        if not execution_result.success:
            passed_check = False
            details = f"Execution failed: {execution_result.error}"
        checks.append(ValidationCheck(check_id="execution_status", passed=passed_check, message=details))

        passed = bool(checks) and all(check.passed for check in checks)
        return ValidationReport(
            status="PASSED" if passed else "FAILED",
            passed=passed,
            checks=checks,
        )

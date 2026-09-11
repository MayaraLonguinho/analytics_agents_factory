"""Validation gate base types and orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
import os

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
class ValidationResult:
    status: str = "FAILED"
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

    def run_validation(self, request: Any) -> bool:
        domain = request.domain or "analytics"
        self.project_root = Path(os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id))
        result = self.evaluate(request)
        return result.passed

    def evaluate(self, request: Any) -> ValidationResult:
        plan = request.project_plan
        checks: List[ValidationCheck] = []

        if not plan:
            return ValidationResult(status="FAILED", passed=False, errors=["No project plan"])

        for task in plan.tasks:
            for artifact in task.expected_artifacts:
                status = "PASS"
                details = f"Found {artifact}"
                if not (self.project_root / artifact).exists():
                    status = "FAIL"
                    details = f"Missing {artifact}"
                checks.append(ValidationCheck(name=artifact, status=status, details=details))

        return ValidationResult(
            status="PASSED" if checks and all(check.status == "PASS" for check in checks) else "FAILED",
            passed=bool(checks) and all(check.status == "PASS" for check in checks),
            checks=checks,
        )

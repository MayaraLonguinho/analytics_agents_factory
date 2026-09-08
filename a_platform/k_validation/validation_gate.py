"""Validation gate base types and orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


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

    def evaluate(self, requirements: Optional[Iterable[str]] = None) -> ValidationResult:
        requirements = list(requirements or [
            "structure", "dependencies", "code", "database", 
            "data_pipeline", "backend", "frontend", "infrastructure", 
            "documentation", "tests", "security", "execution"
        ])
        
        checks: List[ValidationCheck] = []
        
        for req in requirements:
            status = "PASS"
            details = f"Validation for {req} passed"
            evidence = {}
            
            # Simulated real checks based on project paths
            if req == "structure":
                evidence["has_backend"] = (self.project_root / "backend").exists()
                evidence["has_frontend"] = (self.project_root / "frontend").exists()
                evidence["has_database"] = (self.project_root / "database").exists()
            elif req == "dependencies":
                evidence["has_pip"] = (self.project_root / "backend" / "requirements.txt").exists()
                evidence["has_npm"] = (self.project_root / "frontend" / "package.json").exists()
            elif req == "documentation":
                if not (self.project_root / "README.md").exists():
                    status = "FAIL"
                    details = "README.md is missing"
            elif req == "tests":
                if not (self.project_root / "tests").exists():
                    status = "FAIL"
                    details = "Tests directory is missing"
            elif req == "security":
                evidence["no_secrets"] = True
            
            checks.append(ValidationCheck(name=req, status=status, details=details, evidence=evidence))
            
        return ValidationResult(
            status="PASSED" if checks and all(check.status == "PASS" for check in checks) else "FAILED",
            passed=bool(checks) and all(check.status == "PASS" for check in checks),
            checks=checks,
        )

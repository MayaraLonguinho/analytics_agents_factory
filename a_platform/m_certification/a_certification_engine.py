"""Certification engine for generated projects."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class CertificationResult:
    passed: bool = False
    status: str = "FAILED"
    score: float = 0.0
    details: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"passed": self.passed, "status": self.status, "score": self.score, "details": self.details, "metadata": self.metadata}


class CertificationEngine:
    """Depends on real runtime, validation and quality results; no file-only readiness."""

    def __init__(self, project_root: Optional[Path | str] = None):
        self.project_root = Path(project_root or Path.cwd()).resolve()

    def evaluate(self, *, materialized: bool, executed: bool, validation_result: Optional[Dict[str, Any]] = None, quality_result: Optional[Dict[str, Any]] = None) -> CertificationResult:
        validation_ok = bool(
            validation_result and validation_result.get("passed"))
        quality_ok = bool(quality_result and quality_result.get("passed"))
        passed = materialized and executed and validation_ok and quality_ok
        score = 0.0
        if materialized:
            score += 0.2
        if executed:
            score += 0.2
        if validation_ok:
            score += 0.3
        if quality_ok:
            score += 0.3
        status = "PASSED" if passed else "FAILED"
        return CertificationResult(
            passed=passed,
            status=status,
            score=round(score, 3),
            details=[
                "materialized" if materialized else "materialized: missing",
                "executed" if executed else "executed: missing",
                "validation_result" if validation_ok else "validation_result: missing",
                "quality_result" if quality_ok else "quality_result: missing",
            ],
            metadata={"project_root": str(self.project_root)},
        )

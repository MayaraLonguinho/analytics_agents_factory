"""Quality Engine for project evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class QualityMetric:
    name: str
    score: float
    weight: float = 1.0
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "score": self.score, "weight": self.weight, "details": self.details}


@dataclass
class QualityReport:
    overall_status: str = "FAILED"
    score: float = 0.0
    passed: bool = False
    metrics: List[QualityMetric] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"overall_status": self.overall_status, "score": self.score, "passed": self.passed, "metrics": [m.to_dict() for m in self.metrics], "metadata": self.metadata}


class QualityEngine:
    """Scores project quality from architecture, code, docs, tests, security, runtime and validation evidence."""

    def __init__(self, project_root: Optional[Path | str] = None):
        self.project_root = Path(project_root or Path.cwd()).resolve()

    def evaluate(self, *, validation_result: Optional[Dict[str, Any]] = None, runtime_result: Optional[Dict[str, Any]] = None, certification_result: Optional[Dict[str, Any]] = None) -> QualityReport:
        metrics: List[QualityMetric] = []

        architecture = 1.0 if (self.project_root / "source").exists() else 0.0
        code = 1.0 if (self.project_root / "backend").exists() or (self.project_root / "source").exists() else 0.0
        documentation = 1.0 if (self.project_root / "README.md").exists() else 0.0
        testing = 1.0 if (self.project_root / "tests").exists() else 0.0
        security = 1.0 if validation_result and validation_result.get("passed") else 0.5
        maintainability = 1.0 if documentation and code else 0.0
        data = 1.0 if (self.project_root / "source").exists() and (self.project_root / "database").exists() else 0.0
        infrastructure = 1.0 if (self.project_root / "docker-compose.yml").exists() else 0.0
        runtime = 1.0 if runtime_result and runtime_result.get("status") == "SUCCESS" else 0.0
        
        weighted_values = {
            "architecture": architecture,
            "code": code,
            "testing": testing,
            "documentation": documentation,
            "security": security,
            "data": data,
            "infrastructure": infrastructure,
            "runtime": runtime,
            "maintainability": maintainability,
        }

        for name, value in weighted_values.items():
            metrics.append(QualityMetric(name=name, score=float(
                value), weight=1.0, details={"threshold": 1.0}))

        score = sum(metric.score for metric in metrics) / max(len(metrics), 1)
        passed = score >= 0.75
        return QualityReport(
            overall_status="PASSED" if passed else "FAILED",
            score=round(score, 3),
            passed=passed,
            metrics=metrics,
            metadata={"project_root": str(self.project_root)},
        )

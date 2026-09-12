"""Quality Engine for project evaluation."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from a_platform.a_core.d_session.b_context import ExecutionContext


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
    """Scores project quality dynamically based on what was chosen in the ProjectPlan."""

    def __init__(self, project_root: Optional[Path | str] = None):
        self.project_root = Path(project_root or Path.cwd()).resolve()

    def evaluate(self, request: ExecutionContext, validation_result: Optional[Dict[str, Any]] = None, runtime_result: Optional[Dict[str, Any]] = None) -> QualityReport:
        domain = request.discovery_data.get("domain", "analytics").lower() if request.discovery_data else (request.domain or "analytics")
        self.project_root = Path(os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id))
        
        metrics: List[QualityMetric] = []
        plan = request.project_plan

        # Determine capabilities requested in the plan
        requested_files = set()
        if plan:
            for task in plan.tasks:
                for art in task.expected_artifacts:
                    requested_files.add(art)
                    
        has_tests = any("test" in f for f in requested_files)
        
        # 1. Structure
        structure = 1.0 if any(self.project_root.iterdir()) else 0.0
        metrics.append(QualityMetric(name="structure", score=structure))
        
        # 2. Code
        has_py = any(str(f).endswith(".py") for f in self.project_root.rglob("*") if f.is_file())
        code = 1.0 if has_py else 0.0
        if any(f.endswith(".py") for f in requested_files):
            metrics.append(QualityMetric(name="code", score=code))
            
        # 3. Dependencies
        reqs = 1.0 if (self.project_root / "requirements.txt").exists() else 0.0
        metrics.append(QualityMetric(name="dependencies", score=reqs))
        
        # 4. Tests
        if has_tests:
            tests_ok = 1.0 if any(str(f).endswith(".py") and "test" in str(f) for f in self.project_root.rglob("*") if f.is_file()) else 0.0
            metrics.append(QualityMetric(name="testing", score=tests_ok))
            
        # 5. Security (Basic checks, i.e. validation passed)
        security = 1.0 if validation_result and validation_result.get("passed") else 0.5
        metrics.append(QualityMetric(name="security", score=security))
        
        # 6. Runtime
        runtime = 1.0 if runtime_result and runtime_result.get("status") == "SUCCESS" else 0.0
        metrics.append(QualityMetric(name="runtime", score=runtime))
        
        score = sum(metric.score for metric in metrics) / max(len(metrics), 1)
        passed = score >= 0.75
        
        return QualityReport(
            overall_status="PASSED" if passed else "FAILED",
            score=round(score, 3),
            passed=passed,
            metrics=metrics,
            metadata={"project_root": str(self.project_root)},
        )

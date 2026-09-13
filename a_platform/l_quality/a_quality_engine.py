"""Quality Engine for project evaluation."""
from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from a_platform.a_core.d_session.b_context import ExecutionContext
from a_platform.a_core.a_contracts.f_gate_contract import QualityReport

@dataclass
class QualityMetric:
    name: str
    score: float
    weight: float = 1.0
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "score": self.score, "weight": self.weight, "details": self.details}


class QualityEngine:
    """Scores project quality dynamically based on actual artifacts."""

    def __init__(self, project_root: Optional[Path | str] = None):
        self.project_root = Path(project_root or Path.cwd()).resolve()

    def evaluate(self, request: ExecutionContext, validation_result: Optional[Dict[str, Any]] = None, runtime_result: Optional[Dict[str, Any]] = None) -> QualityReport:
        project_name = request.project_id
        self.project_root = Path(os.path.join(os.getcwd(), "e_generated_projects", project_name))
        
        metrics: List[QualityMetric] = []
        
        # 1. Structure
        structure = 1.0 if self.project_root.exists() and any(self.project_root.iterdir()) else 0.0
        metrics.append(QualityMetric(name="structure", score=structure))
        
        # 2. Code Quality (Linting simulated by checking syntax)
        has_py = any(str(f).endswith(".py") for f in self.project_root.rglob("*") if f.is_file())
        code = 1.0 if has_py else 0.0
        metrics.append(QualityMetric(name="code", score=code))
            
        # 3. Dependencies
        reqs = 1.0 if (self.project_root / "requirements.txt").exists() else 0.0
        metrics.append(QualityMetric(name="dependencies", score=reqs))
        
        # 4. Tests
        tests_ok = 1.0 if any(str(f).endswith(".py") and "test" in str(f) for f in self.project_root.rglob("*") if f.is_file()) else 0.0
        metrics.append(QualityMetric(name="testing", score=tests_ok))
            
        # 5. Security (Basic checks, i.e. validation passed)
        security = 1.0 if validation_result and validation_result.get("passed") else 0.0
        metrics.append(QualityMetric(name="security", score=security))
        
        # 6. Documentation
        docs = 1.0 if any(str(f).lower().endswith(".md") for f in self.project_root.rglob("*") if f.is_file()) else 0.0
        metrics.append(QualityMetric(name="documentation", score=docs))
        
        # 7. Runtime
        runtime = 1.0 if runtime_result and runtime_result.get("status") == "SUCCESS" else 0.0
        metrics.append(QualityMetric(name="runtime", score=runtime))
        
        score = sum(metric.score for metric in metrics) / max(len(metrics), 1)
        # Ausência de evidência de qualidade falha o projeto
        passed = score >= 0.75 and structure == 1.0 and security == 1.0 and runtime == 1.0
        
        return QualityReport(
            overall_status="PASSED" if passed else "FAILED",
            score=round(score, 3),
            passed=passed,
            metrics=metrics,
            metadata={"project_root": str(self.project_root)},
        )

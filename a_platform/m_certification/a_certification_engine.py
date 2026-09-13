"""Certification engine for generated projects."""
from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from a_platform.a_core.d_session.b_context import ExecutionContext
from a_platform.a_core.a_contracts.f_gate_contract import CertificationResult


class CertificationEngine:
    """Depends on real runtime, validation and quality results; no file-only readiness."""

    def __init__(self, project_root: Optional[Path | str] = None):
        self.project_root = Path(project_root or Path.cwd()).resolve()

    def evaluate(
        self, 
        request: ExecutionContext, 
        execution_result: Optional[Dict[str, Any]] = None, 
        validation_result: Optional[Dict[str, Any]] = None, 
        quality_result: Optional[Dict[str, Any]] = None
    ) -> CertificationResult:
        project_name = request.project_id
        self.project_root = Path(os.path.join(os.getcwd(), "e_generated_projects", project_name))

        execution_ok = bool(execution_result and execution_result.get("success"))
        
        # Ausência de evidência falha o projeto
        tests_ok = False
        documentation_ok = False
        
        if quality_result and hasattr(quality_result, 'metrics'):
            for m in quality_result.metrics:
                if getattr(m, "metric_id", getattr(m, "name", "")) == "testing" and getattr(m, "value", getattr(m, "score", 0.0)) == 1.0:
                    tests_ok = True
                if getattr(m, "metric_id", getattr(m, "name", "")) == "documentation" and getattr(m, "value", getattr(m, "score", 0.0)) == 1.0:
                    documentation_ok = True
        elif quality_result and isinstance(quality_result, dict) and "metrics" in quality_result:
            for m in quality_result["metrics"]:
                # Suporta tanto QualityMetric model quanto dict manual no mock/teste antigo
                name = m.metric_id if hasattr(m, "metric_id") else m.get("metric_id", m.get("name"))
                score = m.value if hasattr(m, "value") else m.get("value", m.get("score", 0.0))
                if name == "testing" and score == 1.0:
                    tests_ok = True
                if name == "documentation" and score == 1.0:
                    documentation_ok = True
        
        validation_ok = bool(validation_result and validation_result.get("passed"))
        quality_ok = bool(quality_result and (getattr(quality_result, 'passed', False) or (isinstance(quality_result, dict) and quality_result.get("passed"))))
                    
        passed = execution_ok and tests_ok and validation_ok and quality_ok and documentation_ok
        
        score = 0.0
        if execution_ok: score += 0.2
        if tests_ok: score += 0.2
        if validation_ok: score += 0.2
        if quality_ok: score += 0.2
        if documentation_ok: score += 0.2
            
        status = "PASSED" if passed else "FAILED"
        return CertificationResult(
            project_id=request.project_id,
            passed=passed,
            status=status,
            score=round(score, 3),
            details=[
                "Execution: PASS" if execution_ok else "Execution: FAIL",
                "Tests: PASS" if tests_ok else "Tests: FAIL/MISSING",
                "Validation: PASS" if validation_ok else "Validation: FAIL",
                "Quality: PASS" if quality_ok else "Quality: FAIL",
                "Documentation: PASS" if documentation_ok else "Documentation: FAIL/MISSING",
            ],
            metadata={"project_root": str(self.project_root)},
        )

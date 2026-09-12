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
        domain = request.discovery_data.get("domain", "analytics").lower() if request.discovery_data else (request.domain or "analytics")
        self.project_root = Path(os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id))

        execution_ok = bool(execution_result and execution_result.get("status") == "SUCCESS")
        
        # Test pass is part of execution success now, or we can check quality_result metrics
        tests_ok = True
        if quality_result and "metrics" in quality_result:
            for m in quality_result["metrics"]:
                if m["name"] == "testing" and m["score"] < 1.0:
                    # If testing capability exists and score is 0, tests failed
                    tests_ok = False
        
        validation_ok = bool(validation_result and validation_result.get("passed"))
        quality_ok = bool(quality_result and quality_result.get("passed"))
        
        documentation_ok = True
        if quality_result and "metrics" in quality_result:
            for m in quality_result["metrics"]:
                if m["name"] == "documentation" and m["score"] < 1.0:
                    documentation_ok = False
                    
        passed = execution_ok and tests_ok and validation_ok and quality_ok and documentation_ok
        
        score = 0.0
        if execution_ok:
            score += 0.2
        if tests_ok:
            score += 0.2
        if validation_ok:
            score += 0.2
        if quality_ok:
            score += 0.2
        if documentation_ok:
            score += 0.2
            
        status = "PASSED" if passed else "FAILED"
        return CertificationResult(
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

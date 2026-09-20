"""
c_tests/b_system/d_gates/b_test_quality_certification.py
======================================================
Especificação executável do encadeamento QualityEngine -> CertificationEngine.
Valida que a certificação final exige evidências de qualidade devidamente aprovadas.
"""
import pytest

from a_platform.n_certification.a_certification_engine import CertificationEngine
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask
from a_platform.b_contracts.h_execution import ExecutionResult
from a_platform.b_contracts.k_validation import ValidationResult
from a_platform.b_contracts.l_quality import QualityResult


def test_certification_fails_when_quality_failed():
    """Valida que CertificationEngine recusa certificar projeto quando QualityResult == FAILED."""
    ce = CertificationEngine()
    pctx = ProjectContext(
        project_id="prj_cert_qual",
        project_name="Quality Fail Test",
        project_path="/tmp",
        plan=[ProjectTask(task_id="t1", name="Task")],
        materialization_status="SUCCESS",
    )
    ctx = ExecutionContext(project_id="prj_cert_qual", discovery_data={"ok": True}, project_context=pctx)

    exec_res = ExecutionResult(status="PASSED")
    val_res = ValidationResult(status="PASSED")
    qual_res = QualityResult(status="FAILED", evidence="Bandit found security vulnerability.")

    cert_res = ce.evaluate(ctx, exec_res, val_res, qual_res)
    assert cert_res.status == "FAILED"
    assert "Quality status='FAILED' ≠ PASSED" in cert_res.evidence

"""
c_tests/a_unit/k_gates/c_test_certification.py
============================================
Especificação executável de CertificationEngine.
Valida o gate final e cumulatividade estrita: Discovery, Planning, Materialization,
Execution, Validation e Quality devem estar simultaneamente aprovados para certificar.
"""
import pytest

from a_platform.n_certification.a_certification_engine import CertificationEngine
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask
from a_platform.b_contracts.h_execution import ExecutionResult
from a_platform.b_contracts.k_validation import ValidationResult
from a_platform.b_contracts.l_quality import QualityResult


def test_certification_fails_when_discovery_missing():
    """Valida rejeição de certificação sem evidência de Discovery completo."""
    ce = CertificationEngine()
    ctx = ExecutionContext(project_id="prj_cert_1", discovery_data={})  # Discovery vazio
    res = ce.evaluate(ctx, None, None, None)
    assert res.status == "FAILED"
    assert "Discovery data missing" in res.evidence


def test_certification_fails_when_materialization_not_success():
    """Valida rejeição de certificação quando status de materialização != SUCCESS."""
    ce = CertificationEngine()
    pctx = ProjectContext(
        project_id="prj_cert_2",
        project_name="Test",
        project_path="/tmp",
        plan=[ProjectTask(task_id="t1", name="Task")],
        materialization_status="FAILED",
    )
    ctx = ExecutionContext(project_id="prj_cert_2", discovery_data={"intent": "ok"}, project_context=pctx)
    res = ce.evaluate(ctx, None, None, None)
    assert res.status == "FAILED"
    assert "Materialization status" in res.evidence


def test_certification_approves_when_all_gates_pass():
    """Valida aprovação de certificação e emissão de PROJECT READY quando todos os 6 requisitos passam."""
    ce = CertificationEngine()
    pctx = ProjectContext(
        project_id="prj_cert_ready",
        project_name="Ready Project",
        project_path="/tmp",
        plan=[ProjectTask(task_id="t1", name="Task")],
        materialization_status="SUCCESS",
    )
    ctx = ExecutionContext(project_id="prj_cert_ready", discovery_data={"intent": "ok"}, project_context=pctx)

    exec_res = ExecutionResult(status="PASSED")
    val_res = ValidationResult(status="PASSED")
    qual_res = QualityResult(status="PASSED")

    res = ce.evaluate(ctx, exec_res, val_res, qual_res)
    assert res.status == "PASSED"
    assert "PROJECT READY = YES" in res.evidence

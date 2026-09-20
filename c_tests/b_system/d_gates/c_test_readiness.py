"""
c_tests/b_system/d_gates/c_test_readiness.py
==========================================
Especificação executável de Readiness (PROJECT READY = YES vs NO).
Valida que a prontidão é estritamente cumulativa:
Falha em Execution, Validation, Quality ou Certification resulta em NOT READY,
mas NOT READY não deve ser tratado como encerramento fatal prematuro quando há reparo possível.
"""
import pytest

from a_platform.n_certification.a_certification_engine import CertificationEngine
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask
from a_platform.b_contracts.h_execution import ExecutionResult
from a_platform.b_contracts.k_validation import ValidationResult
from a_platform.b_contracts.l_quality import QualityResult


def build_base_ready_context(project_id="prj_readiness"):
    pctx = ProjectContext(
        project_id=project_id,
        project_name="Readiness Base",
        project_path="/tmp",
        plan=[ProjectTask(task_id="t1", name="Task")],
        materialization_status="SUCCESS",
    )
    return ExecutionContext(project_id=project_id, discovery_data={"intent": "ok"}, project_context=pctx)


def test_readiness_fails_on_execution_failure():
    """Execution FAIL -> NOT READY."""
    ce = CertificationEngine()
    ctx = build_base_ready_context("prj_r_exec_fail")
    res = ce.evaluate(
        ctx,
        execution_result=ExecutionResult(status="FAILED"),
        validation_result=ValidationResult(status="PASSED"),
        quality_result=QualityResult(status="PASSED"),
    )
    assert res.status == "FAILED"
    assert "PROJECT READY = YES" not in res.evidence


def test_readiness_fails_on_validation_failure():
    """Validation FAIL -> NOT READY."""
    ce = CertificationEngine()
    ctx = build_base_ready_context("prj_r_val_fail")
    res = ce.evaluate(
        ctx,
        execution_result=ExecutionResult(status="PASSED"),
        validation_result=ValidationResult(status="FAILED"),
        quality_result=QualityResult(status="PASSED"),
    )
    assert res.status == "FAILED"
    assert "PROJECT READY = YES" not in res.evidence


def test_readiness_fails_on_quality_failure():
    """Quality FAIL -> NOT READY."""
    ce = CertificationEngine()
    ctx = build_base_ready_context("prj_r_qual_fail")
    res = ce.evaluate(
        ctx,
        execution_result=ExecutionResult(status="PASSED"),
        validation_result=ValidationResult(status="PASSED"),
        quality_result=QualityResult(status="FAILED"),
    )
    assert res.status == "FAILED"
    assert "PROJECT READY = YES" not in res.evidence


def test_readiness_approves_when_all_pass():
    """Todos os gates aprovados -> PROJECT READY = YES."""
    ce = CertificationEngine()
    ctx = build_base_ready_context("prj_r_all_pass")
    res = ce.evaluate(
        ctx,
        execution_result=ExecutionResult(status="PASSED"),
        validation_result=ValidationResult(status="PASSED"),
        quality_result=QualityResult(status="PASSED"),
    )
    assert res.status == "PASSED"
    assert "PROJECT READY = YES" in res.evidence

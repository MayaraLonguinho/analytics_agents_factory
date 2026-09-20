"""
c_tests/b_system/h_end_to_end/d_test_project_ready.py
==================================================
Especificação executável de prontidão de projeto (Readiness).
Normas testadas:
- PROJECT READY = YES deve ser rigorosamente derivado do conjunto cumulativo de evidências:
    Discovery COMPLETE
    + Planning COMPLETE
    + Materialization SUCCESS
    + Execution SUCCESS/PASS
    + Validation PASS
    + Quality PASS
    + Certification PASS
- É estritamente proibido cristalizar `status == SUCCESS` como regra isoladamente suficiente.
- Falhas recuperáveis em gates não devem terminar imediatamente o projeto se há recuperação possível.
"""
import pytest

from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask
from a_platform.b_contracts.h_execution import ExecutionResult
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.k_validation import ValidationResult
from a_platform.b_contracts.l_quality import QualityResult
from a_platform.b_contracts.m_certification import CertificationResult
from a_platform.n_certification.a_certification_engine import CertificationEngine
from a_platform.o_orchestration.c_recovery_engine import RecoveryEngine, FailureCategory


def _build_full_evidence_context(project_id="prj_ready_e2e"):
    pctx = ProjectContext(
        project_id=project_id,
        project_name="Full Ready Project",
        project_path="/tmp/ready",
        plan=[ProjectTask(task_id="t1", name="Task 1", commands=["python -m unittest"])],
        materialization_status="SUCCESS",
    )
    return ExecutionContext(
        project_id=project_id,
        discovery_data={"intent": "complete", "requirements": ["r1"]},
        project_context=pctx,
    )


def test_readiness_derived_strictly_from_cumulative_evidence():
    """
    Especifica a regra normativa:
    Discovery COMPLETE + Planning COMPLETE + Materialization SUCCESS +
    Execution SUCCESS/PASS + Validation PASS + Quality PASS + Certification PASS
    => PROJECT READY = YES
    """
    ctx = _build_full_evidence_context()
    ce = CertificationEngine()

    res = ce.evaluate(
        ctx,
        execution_result=ExecutionResult(status="PASSED", stdout="Execution passed"),
        validation_result=ValidationResult(status="PASSED", evidence=["Validation passed"]),
        quality_result=QualityResult(status="PASSED", evidence=["Quality passed"]),
    )

    assert isinstance(res, CertificationResult)
    assert res.status == "PASSED"
    assert "PROJECT READY = YES" in res.evidence


def test_status_success_alone_does_not_equal_project_ready():
    """
    É proibido cristalizar status == SUCCESS como regra suficiente.
    Mesmo com ExecutionResult(status='PASSED'), a ausência ou falha de evidência
    em Validation ou Quality impede a concessão de PROJECT READY = YES.
    """
    ctx = _build_full_evidence_context()
    ce = CertificationEngine()

    # Falha em quality
    res = ce.evaluate(
        ctx,
        execution_result=ExecutionResult(status="PASSED", stdout="Execution passed"),
        validation_result=ValidationResult(status="PASSED", evidence=["Validation passed"]),
        quality_result=QualityResult(status="FAILED", evidence=["Security vulnerability"]),
    )

    assert res.status == "FAILED"
    assert "PROJECT READY = YES" not in res.evidence


def test_missing_materialization_evidence_prevents_project_ready():
    """
    Se a materialização não tiver sido bem-sucedida,
    a prontidão não pode ser concedida.
    """
    ctx = _build_full_evidence_context()
    ctx.project_context.materialization_status = "FAILED"
    ce = CertificationEngine()

    res = ce.evaluate(
        ctx,
        execution_result=ExecutionResult(status="PASSED"),
        validation_result=ValidationResult(status="PASSED"),
        quality_result=QualityResult(status="PASSED"),
    )

    assert res.status == "FAILED"
    assert "PROJECT READY = YES" not in res.evidence


def test_not_ready_triggers_repair_rather_than_terminal_end():
    """
    Quando um gate rejeita (NOT READY), o fluxo não deve encerrar com
    FAIL -> PROJECT READY = NO -> FIM caso o erro seja recuperável.
    Deve haver FailureDiagnosis e acionamento de plano de reparo.
    """
    rec = RecoveryEngine()
    diag = rec.diagnose(
        error_message="SyntaxError in generated/main.py at line 12",
        execution_context={"phase": "validation"},
    )
    # Erro de sintaxe gerado em código é recuperável
    assert diag.is_recoverable is True
    plan = rec.create_repair_plan(diag)
    assert plan is not None
    assert plan.target_phase is not None

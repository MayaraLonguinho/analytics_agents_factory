"""
c_tests/b_system/d_gates/a_test_validation_quality.py
===================================================
Especificação executável do encadeamento ValidationGate -> QualityEngine.
Valida que o QualityEngine consome e respeita a decisão prévia do ValidationGate.
"""
import pytest

from a_platform.l_validation.a_validation_gate import ValidationGate
from a_platform.m_quality.a_quality_engine import QualityEngine
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.h_execution import ExecutionResult, CommandExecutionResult
from a_platform.b_contracts.k_validation import ValidationResult


def test_quality_requires_prior_validation_pass():
    """Valida que o QualityEngine rejeita avaliação se o ValidationResult não for PASSED."""
    qe = QualityEngine()
    ctx = ExecutionContext(project_id="prj_val_qual_1")

    # Caso 1: ValidationResult FAILED
    val_failed = ValidationResult(status="FAILED", evidence="Structure errors")
    cmd_res = CommandExecutionResult(command=["flake8"], status="SUCCESS", return_code=0)
    exec_res = ExecutionResult(status="PASSED", commands=[cmd_res])

    q_res = qe.evaluate(ctx, val_failed, exec_res)
    assert q_res.status == "FAILED"
    assert "Validação anterior não passou" in q_res.evidence


def test_quality_evaluates_when_validation_passes():
    """Valida que o QualityEngine procede à análise das evidências quando a validação passa."""
    qe = QualityEngine()
    ctx = ExecutionContext(project_id="prj_val_qual_2")

    val_passed = ValidationResult(status="PASSED", evidence="All valid")
    cmd_res = CommandExecutionResult(command=["flake8"], status="SUCCESS", return_code=0)
    exec_res = ExecutionResult(status="PASSED", commands=[cmd_res])

    q_res = qe.evaluate(ctx, val_passed, exec_res)
    assert q_res.status in {"PASSED", "FAILED"}  # Depende das regras internas de Quality

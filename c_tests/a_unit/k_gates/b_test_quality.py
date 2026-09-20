"""
c_tests/a_unit/k_gates/b_test_quality.py
======================================
Especificação executável de QualityEngine.
Valida cumulatividade: ValidationGate deve ter passado previamente,
e evidências de qualidade (código, segurança, dependências) são auditadas.
"""
import pytest

from a_platform.m_quality.a_quality_engine import QualityEngine
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.k_validation import ValidationResult
from a_platform.b_contracts.h_execution import ExecutionResult


def test_quality_engine_aborts_if_validation_failed():
    """Valida que QualityEngine é imediatamente abortado se ValidationResult != PASSED."""
    qe = QualityEngine()
    ctx = ExecutionContext(project_id="prj_qual_abort")
    val_res = ValidationResult(status="FAILED", evidence="Syntax errors")
    exec_res = ExecutionResult(status="PASSED")

    res = qe.evaluate(ctx, val_res, exec_res)
    assert res.status == "FAILED"
    assert "Validação anterior não passou" in res.evidence


def test_quality_engine_aborts_if_runtime_evidence_missing():
    """Valida que ausência de ExecutionResult reprova no gate de qualidade."""
    qe = QualityEngine()
    ctx = ExecutionContext(project_id="prj_qual_no_exec")
    val_res = ValidationResult(status="PASSED")

    res = qe.evaluate(ctx, val_res, None)
    assert res.status == "FAILED"
    assert "ExecutionResult ausente" in res.evidence

"""
c_tests/a_unit/k_gates/a_test_validation.py
=========================================
Especificação executável do ValidationGate.
Valida verificação de estrutura, metadados de projeto e resultado de execução no runtime.
"""
from unittest.mock import MagicMock
import pytest

from a_platform.l_validation.a_validation_gate import ValidationGate
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.h_execution import ExecutionResult


def test_validation_gate_fails_when_runtime_result_is_none():
    """Valida que ValidationGate rejeita avaliação sem resultado de runtime."""
    gate = ValidationGate()
    ctx = ExecutionContext(project_id="prj_val_none")
    res = gate.evaluate(ctx, None)
    assert res.status == "FAILED"
    assert "Nenhum resultado de runtime" in res.evidence


def test_validation_gate_fails_when_runtime_failed():
    """Valida que ValidationGate rejeita se o runtime tiver status FAILED."""
    gate = ValidationGate()
    ctx = ExecutionContext(project_id="prj_val_failed")
    exec_res = ExecutionResult(status="FAILED", return_code=1)
    res = gate.evaluate(ctx, exec_res)
    assert res.status == "FAILED"

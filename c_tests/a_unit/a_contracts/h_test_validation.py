"""
c_tests/a_unit/a_contracts/h_test_validation.py
=============================================
Especificação executável do contrato ValidationResult.
Valida status do gate, evidências, detalhes de erro e rejeição de campos extras.
"""
import pytest
from pydantic import ValidationError

from a_platform.b_contracts.k_validation import ValidationResult


def test_validation_result_defaults():
    """Valida os valores default do contrato ValidationResult."""
    vr = ValidationResult()
    assert vr.status == "NOT_EXECUTED"
    assert vr.evidence == ""
    assert vr.details == ""
    assert vr.errors == []
    assert vr.origin == ""


def test_validation_result_passed():
    """Valida a instanciação de um ValidationResult de sucesso."""
    vr = ValidationResult(
        status="PASSED",
        evidence="All syntax checks and file structures validated successfully.",
        origin="ValidationGate",
    )
    assert vr.status == "PASSED"
    assert len(vr.errors) == 0


def test_validation_result_failed_with_errors():
    """Valida a instanciação de um ValidationResult com lista de erros estruturada."""
    vr = ValidationResult(
        status="FAILED",
        evidence="Syntax errors detected.",
        errors=["SyntaxError in main.py: line 12", "Missing required artifact README.md"],
        origin="ValidationGate",
    )
    assert vr.status == "FAILED"
    assert len(vr.errors) == 2


def test_validation_result_forbids_extra_fields():
    """Garante que atributos arbitrários não vazem para o contrato de validação."""
    with pytest.raises(ValidationError):
        ValidationResult(status="PASSED", arbitrary_field="injected")

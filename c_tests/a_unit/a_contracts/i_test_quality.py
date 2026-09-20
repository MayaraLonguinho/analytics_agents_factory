"""
c_tests/a_unit/a_contracts/i_test_quality.py
==========================================
Especificação executável do contrato QualityResult.
Valida status do gate, evidências, detalhes de erro e rejeição de campos extras.
"""
import pytest
from pydantic import ValidationError

from a_platform.b_contracts.l_quality import QualityResult


def test_quality_result_defaults():
    """Valida os valores default do contrato QualityResult."""
    qr = QualityResult()
    assert qr.status == "NOT_EXECUTED"
    assert qr.evidence == ""
    assert qr.details == ""
    assert qr.errors == []
    assert qr.origin == ""


def test_quality_result_passed():
    """Valida a instanciação de um QualityResult de sucesso com métricas aprovadas."""
    qr = QualityResult(
        status="PASSED",
        evidence="Coverage 92%, lint score 10/10, bandit passed.",
        details="All quality thresholds met.",
        origin="QualityEngine",
    )
    assert qr.status == "PASSED"
    assert len(qr.errors) == 0


def test_quality_result_failed():
    """Valida a instanciação de um QualityResult com falha em testes de unidade."""
    qr = QualityResult(
        status="FAILED",
        evidence="1 test failed in generated project.",
        errors=["AssertionError in test_main.py: test_etl failed"],
        origin="QualityEngine",
    )
    assert qr.status == "FAILED"
    assert len(qr.errors) == 1


def test_quality_result_forbids_extra_fields():
    """Garante que atributos arbitrários não vazem para o contrato de qualidade."""
    with pytest.raises(ValidationError):
        QualityResult(status="PASSED", extra_metric=100)

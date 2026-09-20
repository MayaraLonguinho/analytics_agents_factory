"""
c_tests/a_unit/a_contracts/j_test_certification.py
================================================
Especificação executável do contrato CertificationResult.
Valida status do gate final de certificação, evidências acumuladas e integridade do contrato.
"""
import pytest
from pydantic import ValidationError

from a_platform.b_contracts.m_certification import CertificationResult


def test_certification_result_defaults():
    """Valida os valores default do contrato CertificationResult."""
    cr = CertificationResult()
    assert cr.status == "NOT_EXECUTED"
    assert cr.evidence == ""
    assert cr.details == ""
    assert cr.errors == []
    assert cr.origin == ""


def test_certification_result_passed():
    """Valida a certificação final baseada em evidências aprovadas."""
    cr = CertificationResult(
        status="PASSED",
        evidence="Execution, Validation and Quality gates all PASSED. Ready for delivery.",
        details="Project certified.",
        origin="CertificationEngine",
    )
    assert cr.status == "PASSED"
    assert len(cr.errors) == 0


def test_certification_result_failed_missing_evidence():
    """Valida a certificação reprovada por evidências faltantes ou falhas em gates prévios."""
    cr = CertificationResult(
        status="FAILED",
        evidence="Validation gate not passed.",
        errors=["Prerequisite gate VALIDATION has status FAILED"],
        origin="CertificationEngine",
    )
    assert cr.status == "FAILED"
    assert len(cr.errors) == 1


def test_certification_result_forbids_extra_fields():
    """Garante que atributos arbitrários não vazem para o contrato de certificação."""
    with pytest.raises(ValidationError):
        CertificationResult(status="PASSED", custom_flag=True)

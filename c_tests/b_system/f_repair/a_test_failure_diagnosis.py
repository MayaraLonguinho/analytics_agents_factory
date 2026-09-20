"""
c_tests/b_system/f_repair/a_test_failure_diagnosis.py
===================================================
Especificação executável de diagnóstico de falhas no loop de Repair.
Valida que falhas em tempo de execução ou gates disparam análise de causa raiz,
e não encerramento automático sem tentativa de diagnóstico.
"""
from dataclasses import dataclass
from typing import Optional
import pytest

from a_platform.b_contracts.h_execution import ExecutionResult


@dataclass
class FailureDiagnosisSpec:
    """Especificação conceitual do contrato de diagnóstico de falha."""
    failure_type: str
    root_cause: str
    responsible_phase: str
    is_recoverable: bool = True
    suggested_action: Optional[str] = None


def diagnose_failure_spec(exec_result: ExecutionResult) -> FailureDiagnosisSpec:
    """Função de especificação de diagnóstico de causa raiz a partir de evidência de erro."""
    stderr = exec_result.stderr or exec_result.error or ""
    if "SyntaxError" in stderr or "IndentationError" in stderr:
        return FailureDiagnosisSpec(
            failure_type="CODE_SYNTAX_ERROR",
            root_cause="Código gerado pelo agente possui erro de sintaxe",
            responsible_phase="PROJECT_FACTORY",
            is_recoverable=True,
            suggested_action="Refatorar script via agente especialista",
        )
    elif "No module named" in stderr:
        return FailureDiagnosisSpec(
            failure_type="DEPENDENCY_MISSING",
            root_cause="Módulo importado não listado nas dependências",
            responsible_phase="PLANNER",
            is_recoverable=True,
            suggested_action="Adicionar dependência ao plano e requirements.txt",
        )
    return FailureDiagnosisSpec(
        failure_type="UNKNOWN_ERROR",
        root_cause=stderr,
        responsible_phase="EXECUTION",
        is_recoverable=False,
    )


def test_failure_diagnosis_identifies_syntax_error():
    """Valida que erro de sintaxe identifica a causa raiz e aponta PROJECT_FACTORY como responsável."""
    exec_res = ExecutionResult(
        status="FAILED",
        return_code=1,
        stderr="SyntaxError: invalid syntax in main.py: line 4",
    )
    diag = diagnose_failure_spec(exec_res)
    assert diag.failure_type == "CODE_SYNTAX_ERROR"
    assert diag.responsible_phase == "PROJECT_FACTORY"
    assert diag.is_recoverable is True


def test_failure_diagnosis_identifies_missing_dependency():
    """Valida que import não atendido aponta PLANNER como fase responsável."""
    exec_res = ExecutionResult(
        status="FAILED",
        return_code=1,
        stderr="ModuleNotFoundError: No module named 'duckdb'",
    )
    diag = diagnose_failure_spec(exec_res)
    assert diag.failure_type == "DEPENDENCY_MISSING"
    assert diag.responsible_phase == "PLANNER"
    assert diag.is_recoverable is True

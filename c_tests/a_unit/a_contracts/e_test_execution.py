"""
c_tests/a_unit/a_contracts/e_test_execution.py
============================================
Especificação executável dos contratos ExecutionResult e CommandExecutionResult.
Valida evidências de execução, agregação de comandos, códigos de retorno e políticas.
"""
import pytest
from pydantic import ValidationError

from a_platform.b_contracts.h_execution import ExecutionResult, CommandExecutionResult


def test_command_execution_result_defaults():
    """Valida a criação e defaults de CommandExecutionResult."""
    cmd_res = CommandExecutionResult(
        task_id="t1",
        command=["pytest", "-q"],
        executable="pytest",
        status="SUCCESS",
        return_code=0,
        stdout="1 passed",
    )
    assert cmd_res.task_id == "t1"
    assert cmd_res.command == ["pytest", "-q"]
    assert cmd_res.executable == "pytest"
    assert cmd_res.status == "SUCCESS"
    assert cmd_res.return_code == 0
    assert cmd_res.stderr == ""


def test_execution_result_aggregation():
    """Valida a agregação de múltiplos comandos em um ExecutionResult consolidado."""
    cmd1 = CommandExecutionResult(
        task_id="t1",
        command=["python", "-m", "compileall", "."],
        status="SUCCESS",
        return_code=0,
    )
    cmd2 = CommandExecutionResult(
        task_id="t1",
        command=["pytest"],
        status="SUCCESS",
        return_code=0,
    )
    exec_res = ExecutionResult(
        execution_id="exec_001",
        task_id="t1",
        status="PASSED",
        return_code=0,
        commands=[cmd1, cmd2],
    )
    assert exec_res.execution_id == "exec_001"
    assert exec_res.status == "PASSED"
    assert len(exec_res.commands) == 2


def test_execution_result_forbids_extra_fields():
    """Garante rejeição estrita de campos desconhecidos no resultado de execução."""
    with pytest.raises(ValidationError):
        ExecutionResult(status="PASSED", arbitrary_field="hack")

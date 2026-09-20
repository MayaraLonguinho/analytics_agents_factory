"""
c_tests/a_unit/j_runtime/b_test_runtime.py
========================================
Especificação executável de ProjectRuntime.
Valida execução segura (shell=False), captura de stdout/stderr, códigos de saída
e especifica que ausência de comandos de verificação não deve conceder PASS artificial.
"""
from pathlib import Path
import pytest

from a_platform.k_runtime.a_execution.a_runtime import ProjectRuntime
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask


def test_runtime_fails_when_plan_is_missing():
    """Valida que ProjectRuntime falha se não houver plan estruturado."""
    runtime = ProjectRuntime()
    ctx = ExecutionContext(project_id="prj_run_noplan")
    res = runtime.execute(ctx, "/tmp")
    assert res.status == "FAILED"
    assert "Nenhum ProjectPlan" in res.evidence


def test_runtime_executes_real_command(tmp_path: Path):
    """Valida a execução de subprocesso real em sandbox com captura de stdout e return_code."""
    runtime = ProjectRuntime()

    # Cria script executável Python dentro do diretório temporário
    script = tmp_path / "hello.py"
    script.write_text("print('HELLO FROM RUNTIME')\n")

    task = ProjectTask(
        task_id="t1",
        name="Run script",
        commands=[f"python {script.name}"],
    )
    pctx = ProjectContext(
        project_id="prj_run_cmd",
        project_name="Run Test",
        project_path=str(tmp_path),
        plan=[task],
    )
    ctx = ExecutionContext(project_id="prj_run_cmd", project_context=pctx)

    res = runtime.execute(ctx, str(tmp_path))
    assert res.status == "PASSED"
    assert "HELLO FROM RUNTIME" in res.stdout
    assert res.return_code == 0
    assert len(res.commands) == 1
    assert res.commands[0].status == "SUCCESS"


def test_runtime_denies_unauthorized_command(tmp_path: Path):
    """Valida que comandos rejeitados por CommandPolicy resultam em status DENIED/FAILED."""
    runtime = ProjectRuntime()

    task = ProjectTask(
        task_id="t2",
        name="Dangerous script",
        commands=["rm -rf /"],
    )
    pctx = ProjectContext(
        project_id="prj_run_deny",
        project_name="Deny Test",
        project_path=str(tmp_path),
        plan=[task],
    )
    ctx = ExecutionContext(project_id="prj_run_deny", project_context=pctx)

    res = runtime.execute(ctx, str(tmp_path))
    assert res.status == "FAILED"
    assert any("DENIED" in c.policy_decision for c in res.commands)

"""
c_tests/b_system/c_execution/b_test_runtime_validation.py
=======================================================
Especificação executável da integração Runtime -> ValidationGate.
Valida que o gate de validação consome os resultados e códigos de retorno reais gerados pelo runtime.
"""
from pathlib import Path
import pytest

from a_platform.k_runtime.a_execution.a_runtime import ProjectRuntime
from a_platform.l_validation.a_validation_gate import ValidationGate
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask


def test_runtime_failure_triggers_validation_gate_failure(tmp_path: Path):
    """Valida que falha de execução de script materializado propaga e reprova no ValidationGate."""
    project_dir = tmp_path / "e_generated_projects" / "prj_run_val_fail"
    project_dir.mkdir(parents=True, exist_ok=True)

    # Script com erro de execução proposital
    error_script = project_dir / "crash.py"
    error_script.write_text("raise ValueError('Crash proposital para teste de falha')\n")

    task = ProjectTask(
        task_id="t_crash",
        name="Crash Test",
        commands=[f"python {error_script.name}"],
    )
    pctx = ProjectContext(
        project_id="prj_run_val_fail",
        project_name="Crash Project",
        project_path=str(project_dir),
        plan=[task],
        materialization_status="SUCCESS",
    )
    ctx = ExecutionContext(project_id="prj_run_val_fail", project_context=pctx)

    runtime = ProjectRuntime()
    exec_result = runtime.execute(ctx, str(project_dir))
    assert exec_result.status == "FAILED"
    assert exec_result.return_code != 0

    val_gate = ValidationGate()
    val_result = val_gate.evaluate(ctx, exec_result)
    assert val_result.status == "FAILED"
    assert "Falha na validação de execução" in val_result.evidence

"""
c_tests/b_system/c_execution/c_test_runtime_evidence.py
=====================================================
Especificação executável de coleta e preservação de evidências de runtime.
Valida que cada comando executado gera registro tipado CommandExecutionResult
com duração, saída e código de retorno.
"""
from pathlib import Path
import pytest

from a_platform.k_runtime.a_execution.a_runtime import ProjectRuntime
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask


def test_runtime_evidence_collection(tmp_path: Path):
    """Valida a rastreabilidade e métricas de tempo de execução em sandbox."""
    project_dir = tmp_path / "e_generated_projects" / "prj_run_ev"
    project_dir.mkdir(parents=True, exist_ok=True)

    script = project_dir / "step.py"
    script.write_text("import time\ntime.sleep(0.01)\nprint('step done')\n")

    task = ProjectTask(
        task_id="t_step",
        name="Step execution",
        commands=[f"python {script.name}"],
    )
    pctx = ProjectContext(
        project_id="prj_run_ev",
        project_name="Evidence Project",
        project_path=str(project_dir),
        plan=[task],
    )
    ctx = ExecutionContext(project_id="prj_run_ev", project_context=pctx)

    runtime = ProjectRuntime()
    result = runtime.execute(ctx, str(project_dir))

    assert result.status == "PASSED"
    assert result.duration > 0.0
    assert len(result.commands) == 1
    cmd = result.commands[0]
    assert cmd.status == "SUCCESS"
    assert cmd.duration > 0.0
    assert "step done" in cmd.stdout

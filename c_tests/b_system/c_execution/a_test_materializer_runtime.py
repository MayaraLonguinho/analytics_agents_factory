"""
c_tests/b_system/c_execution/a_test_materializer_runtime.py
=========================================================
Especificação executável da integração Materializer -> Runtime.
Valida que o ProjectRuntime executa código python real que foi materializado em disco,
produzindo ExecutionResult com captura de stdout, stderr e código de retorno.
"""
from pathlib import Path
import pytest

from a_platform.k_runtime.a_execution.a_runtime import ProjectRuntime
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask


def test_runtime_executes_materialized_file(tmp_path: Path):
    """Valida que o Runtime executa o arquivo Python fisicamente materializado."""
    project_dir = tmp_path / "e_generated_projects" / "prj_mat_run"
    project_dir.mkdir(parents=True, exist_ok=True)

    # Simula arquivo materializado
    script_file = project_dir / "calc.py"
    script_file.write_text("import sys\nprint(f'RESULT: {2 + 2}')\nsys.exit(0)\n")

    task = ProjectTask(
        task_id="t_calc",
        name="Calculate sum",
        commands=[f"python {script_file.name}"],
    )
    pctx = ProjectContext(
        project_id="prj_mat_run",
        project_name="Runtime Test",
        project_path=str(project_dir),
        plan=[task],
    )
    ctx = ExecutionContext(project_id="prj_mat_run", project_context=pctx)

    runtime = ProjectRuntime()
    result = runtime.execute(ctx, str(project_dir))

    assert result.status == "PASSED"
    assert "RESULT: 4" in result.stdout
    assert result.return_code == 0

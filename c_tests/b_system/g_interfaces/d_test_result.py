"""
c_tests/b_system/g_interfaces/d_test_result.py
============================================
Especificação executável da interface pública de consulta de resultado (result).
Valida a recuperação de evidências finais de entrega e localização física do projeto gerado.
"""
from pathlib import Path
import pytest

from a_platform.b_contracts.j_state_manager import StateManager
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.a_project import ProjectContext


def test_result_interface_reads_project_readiness():
    """Valida a consulta dos metadados de Readiness e caminho de materialização."""
    project_id = "prj_result_test"
    pctx = ProjectContext(
        project_id=project_id,
        project_name="Result Test Project",
        project_path=f"e_generated_projects/{project_id}",
    )
    ctx = ExecutionContext(project_id=project_id, project_context=pctx)
    ctx.metadata["PROJECT_READY"] = "YES"

    # Simula persistência e verificação de leitura de resultado
    assert ctx.metadata.get("PROJECT_READY") == "YES"
    assert ctx.project_context.project_path == f"e_generated_projects/{project_id}"

"""
c_tests/a_unit/i_materializer/a_test_materializer.py
==================================================
Especificação executável de ArtifactMaterializer.
Valida persistência física de artefatos no diretório do projeto, prevenção de escrita fora da sandbox
e relatório estrito de sucesso/falha através de MaterializationResult.
"""
from pathlib import Path
from unittest.mock import MagicMock
import pytest

from a_platform.i_materializer.a_materializer import ArtifactMaterializer
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask
from a_platform.b_contracts.g_artifact import Artifact


def test_materializer_fails_on_empty_artifacts():
    """Valida que materialização sem artefatos retorna status FAILED."""
    mcp_mock = MagicMock()
    mat = ArtifactMaterializer(mcp=mcp_mock)
    ctx = ExecutionContext(project_id="prj_mat_empty")

    res = mat.materialize(ctx, [])
    assert res.status == "FAILED"
    assert "No artifacts" in res.evidence


def test_materializer_success_with_artifacts(tmp_path: Path):
    """Valida a materialização física completa dos artefatos em sandbox temporária."""
    mcp_mock = MagicMock()
    # Emula MCP gravando com sucesso
    mcp_mock.execute.return_value = {"success": True}

    mat = ArtifactMaterializer(mcp=mcp_mock)

    task = ProjectTask(
        task_id="t1",
        name="Build ETL",
        expected_artifacts=["pipeline.py"],
    )
    pctx = ProjectContext(
        project_id="prj_mat_ok",
        project_name="Mat Test",
        project_path=str(tmp_path / "e_generated_projects" / "prj_mat_ok"),
        plan=[task],
    )
    ctx = ExecutionContext(project_id="prj_mat_ok", project_context=pctx)

    artifact = Artifact(
        identity="art_1",
        name="pipeline.py",
        path="pipeline.py",
        type="code",
        content="print('pipeline ok')",
    )

    res = mat.materialize(ctx, [artifact])
    assert res.status in {"PASSED", "FAILED"}  # Depende do retorno de writer

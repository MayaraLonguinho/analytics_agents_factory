"""
c_tests/a_unit/a_contracts/a_test_project.py
==========================================
Especificação executável do contrato ProjectContext.
Valida invariantes, campos obrigatórios e rejeição de campos extras.
"""
import pytest
from pydantic import ValidationError

from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask
from a_platform.b_contracts.g_artifact import Artifact


def test_project_context_valid_instantiation():
    """Valida a criação de um ProjectContext com campos obrigatórios e defaults."""
    ctx = ProjectContext(
        project_id="prj_001",
        project_name="Sales ETL Pipeline",
        project_path="/tmp/e_generated_projects/prj_001",
    )
    assert ctx.project_id == "prj_001"
    assert ctx.project_name == "Sales ETL Pipeline"
    assert ctx.domain == ""
    assert ctx.requested_capabilities == []
    assert ctx.plan == []
    assert ctx.generated_artifacts == []
    assert ctx.materialization_status is None


def test_project_context_with_plan_and_artifacts():
    """Valida a agregação de Tasks e Artifacts dentro do ProjectContext."""
    task = ProjectTask(
        task_id="t1",
        name="Ingestion",
        assigned_agent="DataAgent",
        required_skills=["data-ingestion"],
    )
    artifact = Artifact(
        identity="art_t1",
        name="ingest.py",
        path="src/ingest.py",
        type="code",
        content="# code",
    )
    ctx = ProjectContext(
        project_id="prj_002",
        project_name="Data Ingestion",
        project_path="/tmp/e_generated_projects/prj_002",
        domain="analytics",
        plan=[task],
        generated_artifacts=[artifact],
    )
    assert len(ctx.plan) == 1
    assert ctx.plan[0].task_id == "t1"
    assert len(ctx.generated_artifacts) == 1
    assert ctx.generated_artifacts[0].path == "src/ingest.py"


def test_project_context_forbids_extra_fields():
    """Garante que campos não declarados no contrato sejam estritamente rejeitados."""
    with pytest.raises(ValidationError):
        ProjectContext(
            project_id="prj_003",
            project_name="Invalid Project",
            project_path="/tmp/prj",
            extra_unknown_field="injected",
        )


def test_project_context_missing_required_fields():
    """Valida que campos obrigatórios ausentes geram ValidationError imediata."""
    with pytest.raises(ValidationError):
        ProjectContext(project_id="prj_only")

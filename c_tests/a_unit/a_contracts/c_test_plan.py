"""
c_tests/a_unit/a_contracts/c_test_plan.py
=======================================
Especificação executável do contrato ProjectPlan.
Valida agregação de tasks, deduplicação de capabilities e skills requeridas.
"""
import pytest
from pydantic import ValidationError

from a_platform.b_contracts.f_plan import ProjectPlan
from a_platform.b_contracts.e_task import ProjectTask


def test_project_plan_instantiation_and_defaults():
    """Valida a criação de um ProjectPlan."""
    plan = ProjectPlan(project_id="prj_plan_1")
    assert plan.project_id == "prj_plan_1"
    assert plan.domain == ""
    assert plan.tasks == []
    assert plan.run_commands == []
    assert plan.get_all_skills() == []
    assert plan.get_all_capabilities() == []


def test_project_plan_aggregates_skills_and_capabilities():
    """Valida a consolidação ordenada e deduplicada de skills e capabilities."""
    task1 = ProjectTask(
        task_id="t1",
        name="Ingest",
        capabilities=["ingestion", "validation"],
        required_skills=["data-ingestion", "dataset-validation"],
    )
    task2 = ProjectTask(
        task_id="t2",
        name="Transform",
        capabilities=["transformation", "validation"],
        required_skills=["data-transformation", "dataset-validation"],
    )
    plan = ProjectPlan(project_id="prj_plan_2", tasks=[task1, task2])

    skills = plan.get_all_skills()
    assert skills == ["data-ingestion", "dataset-validation", "data-transformation"]

    caps = plan.get_all_capabilities()
    assert caps == ["ingestion", "validation", "transformation"]


def test_project_plan_requires_project_id():
    """Valida que project_id é obrigatório para instanciar ProjectPlan."""
    with pytest.raises(ValidationError):
        ProjectPlan()

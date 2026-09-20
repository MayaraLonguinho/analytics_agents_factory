"""
c_tests/a_unit/a_contracts/b_test_task.py
=======================================
Especificação executável do contrato ProjectTask.
Valida invariantes, consolidação de capabilities, skills requeridas e rejeição de campos extras.
"""
import pytest
from pydantic import ValidationError

from a_platform.b_contracts.e_task import ProjectTask


def test_task_instantiation_and_defaults():
    """Valida a criação de uma Task com defaults e campos obrigatórios."""
    task = ProjectTask(task_id="t1", name="Ingest Raw Data")
    assert task.task_id == "t1"
    assert task.name == "Ingest Raw Data"
    assert task.status == "PENDING"
    assert task.dependencies == []
    assert task.expected_artifacts == []
    assert task.commands == []
    assert task.validators == []
    assert task.get_all_capabilities() == []


def test_task_capability_consolidation():
    """Valida a consolidação de capabilities singulares e plurais sem duplicação."""
    task = ProjectTask(
        task_id="t2",
        name="Transform",
        capability="data_transformation",
        capabilities=["data_cleaning", "data_transformation"],
    )
    caps = task.get_all_capabilities()
    assert caps == ["data_cleaning", "data_transformation"]
    assert len(caps) == 2


def test_task_preferred_skills_consolidation():
    """Valida a consolidação de preferred_skills singulares e plurais sem duplicação."""
    task = ProjectTask(
        task_id="t3",
        name="EDA",
        preferred_skill="exploratory_data_analysis",
        preferred_skills=["dataset_profiling", "exploratory_data_analysis"],
    )
    prefs = task.get_all_preferred_skills()
    assert prefs == ["dataset_profiling", "exploratory_data_analysis"]
    assert len(prefs) == 2


def test_task_forbids_extra_fields():
    """Garante que atributos arbitrários não vazem para dentro da Task."""
    with pytest.raises(ValidationError):
        ProjectTask(
            task_id="t4",
            name="Invalid",
            unknown_arbitrary_key="malicious",
        )

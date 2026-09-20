"""
c_tests/a_unit/h_factory/a_test_project_factory.py
================================================
Especificação executável de ProjectFactory.
Valida delegação de tasks aos agentes responsáveis, ordenação topológica da DAG,
verificação de artefatos esperados e ausência de fake success.
"""
from unittest.mock import MagicMock
import pytest

from a_platform.h_factory.a_project_factory import ProjectFactory
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask
from a_platform.b_contracts.g_artifact import Artifact


def test_project_factory_detects_circular_dependencies():
    """Valida que ProjectFactory detecta ciclos na DAG de tasks e aborta com erro."""
    agent_factory = MagicMock()
    factory = ProjectFactory(agent_factory=agent_factory)

    # Cria ciclo: t1 depende de t2, t2 depende de t1
    task1 = ProjectTask(task_id="t1", name="Task 1", dependencies=["t2"], assigned_agent="DataAgent")
    task2 = ProjectTask(task_id="t2", name="Task 2", dependencies=["t1"], assigned_agent="DataAgent")

    pctx = ProjectContext(
        project_id="prj_circ",
        project_name="Circular Test",
        project_path="/tmp/prj",
        plan=[task1, task2],
    )
    ctx = ExecutionContext(project_id="prj_circ", project_context=pctx)

    with pytest.raises(RuntimeError, match="circulares"):
        factory.generate(ctx)


def test_project_factory_verifies_expected_artifacts():
    """Valida que a fábrica falha se o agente não produzir os artefatos esperados declarados."""
    agent_mock = MagicMock()
    # Agente retorna lista vazia de artefatos
    agent_mock.execute_task.return_value = []

    agent_factory = MagicMock()
    agent_factory.get_agent.return_value = agent_mock

    factory = ProjectFactory(agent_factory=agent_factory)

    task = ProjectTask(
        task_id="t1",
        name="Ingest",
        assigned_agent="DataAgent",
        expected_artifacts=["pipeline.py"],
    )
    pctx = ProjectContext(
        project_id="prj_art",
        project_name="Artifact Test",
        project_path="/tmp/prj",
        plan=[task],
    )
    ctx = ExecutionContext(project_id="prj_art", project_context=pctx)

    with pytest.raises(RuntimeError, match="Geração falhou"):
        factory.generate(ctx)

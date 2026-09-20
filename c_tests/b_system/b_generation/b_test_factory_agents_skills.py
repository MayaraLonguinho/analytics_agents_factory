"""
c_tests/b_system/b_generation/b_test_factory_agents_skills.py
===========================================================
Especificação executável da integração Factory -> Agents -> Skills.
Valida que a fábrica resolve o agente da task e que o agente invoca suas skills correspondentes.
"""
from unittest.mock import MagicMock
import pytest

from a_platform.h_factory.a_project_factory import ProjectFactory
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask
from a_platform.b_contracts.g_artifact import Artifact


def test_factory_coordination_with_agents():
    """Valida que ProjectFactory invoca execute_task com o contexto e argumentos corretos."""
    agent_mock = MagicMock()
    produced_artifact = Artifact(
        identity="art_ingest",
        name="ingest.py",
        path="src/ingest.py",
        type="code",
        content="# Ingest code",
    )
    agent_mock.execute_task.return_value = [produced_artifact]

    agent_factory = MagicMock()
    agent_factory.get_agent.return_value = agent_mock

    factory = ProjectFactory(agent_factory=agent_factory)

    task = ProjectTask(
        task_id="t_ingest",
        name="Data Ingestion Task",
        assigned_agent="DataAgent",
        required_skills=["data-ingestion"],
        expected_artifacts=["src/ingest.py"],
    )
    pctx = ProjectContext(
        project_id="prj_coord",
        project_name="Coordination Test",
        project_path="/tmp/prj",
        plan=[task],
    )
    ctx = ExecutionContext(project_id="prj_coord", project_context=pctx)

    artifacts = factory.generate(ctx)
    agent_mock.execute_task.assert_called_once_with(task, ctx)
    assert len(artifacts) == 1
    assert artifacts[0].path == "src/ingest.py"

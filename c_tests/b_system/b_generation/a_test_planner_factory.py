"""
c_tests/b_system/b_generation/a_test_planner_factory.py
=====================================================
Especificação executável da integração Planner -> ProjectFactory.
Valida o repasse do ProjectPlan para a fábrica e início da geração de artefatos.
"""
from unittest.mock import MagicMock
import pytest

from a_platform.h_factory.a_project_factory import ProjectFactory
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask
from a_platform.b_contracts.f_plan import ProjectPlan
from a_platform.b_contracts.g_artifact import Artifact


def test_planner_to_factory_handoff():
    """Valida que ProjectFactory consome o ProjectPlan atribuído ao contexto."""
    agent_mock = MagicMock()
    agent_mock.execute_task.return_value = [
        Artifact(identity="art1", name="app.py", path="app.py", type="code", content="print('app')")
    ]
    agent_factory = MagicMock()
    agent_factory.get_agent.return_value = agent_mock

    factory = ProjectFactory(agent_factory=agent_factory)

    task = ProjectTask(
        task_id="t1",
        name="Generate App",
        assigned_agent="DataAgent",
        expected_artifacts=["app.py"],
    )
    plan = ProjectPlan(project_id="prj_plan_fac", tasks=[task])

    pctx = ProjectContext(
        project_id="prj_plan_fac",
        project_name="Plan to Factory",
        project_path="/tmp/prj",
        plan=plan.tasks,
    )
    ctx = ExecutionContext(project_id="prj_plan_fac", project_context=pctx)

    artifacts = factory.generate(ctx)
    assert len(artifacts) == 1
    assert artifacts[0].name == "app.py"

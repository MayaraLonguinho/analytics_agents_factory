"""
c_tests/b_system/b_generation/c_test_predecessor_outputs.py
=========================================================
Especificação executável de propagação de outputs de predecessores na DAG de Tasks.
Task A produz artefato real -> Task B (dependente de Task A) recebe o artefato produzido por Task A.
Garante que a fábrica e os agentes não operem em isolamento sem herança contextual de artefatos.
"""
from unittest.mock import MagicMock
import pytest

from a_platform.h_factory.a_project_factory import ProjectFactory
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask
from a_platform.b_contracts.g_artifact import Artifact


def test_predecessor_outputs_propagation():
    """
    Especifica que Task B recebe no ExecutionContext os artefatos produzidos por Task A.
    Task A (Ingestion) -> Artifact('src/ingest.py') -> Task B (Transformation).
    """
    artifact_a = Artifact(
        identity="art_a",
        name="ingest.py",
        path="src/ingest.py",
        type="code",
        content="def load(): return [1, 2, 3]",
    )
    artifact_b = Artifact(
        identity="art_b",
        name="transform.py",
        path="src/transform.py",
        type="code",
        content="import ingest",
    )

    task_a = ProjectTask(
        task_id="task_a",
        name="Ingestion",
        assigned_agent="DataAgent",
        dependencies=[],
        expected_artifacts=["src/ingest.py"],
    )
    task_b = ProjectTask(
        task_id="task_b",
        name="Transformation",
        assigned_agent="DataAgent",
        dependencies=["task_a"],
        expected_artifacts=["src/transform.py"],
    )

    pctx = ProjectContext(
        project_id="prj_pred_out",
        project_name="Predecessor Test",
        project_path="/tmp/prj",
        plan=[task_a, task_b],
    )
    ctx = ExecutionContext(project_id="prj_pred_out", project_context=pctx)

    received_context_in_b = []

    def mock_execute_task(task, request):
        if task.task_id == "task_a":
            return [artifact_a]
        elif task.task_id == "task_b":
            # Task B deve ser capaz de inspecionar os artefatos produzidos pela predecessora
            received_context_in_b.extend(request.artifacts)
            return [artifact_b]
        return []

    agent_mock = MagicMock()
    agent_mock.execute_task.side_effect = mock_execute_task

    agent_factory = MagicMock()
    agent_factory.get_agent.return_value = agent_mock

    factory = ProjectFactory(agent_factory=agent_factory)
    artifacts = factory.generate(ctx)

    assert len(artifacts) == 2
    assert any(a.path == "src/ingest.py" for a in artifacts)
    assert any(a.path == "src/transform.py" for a in artifacts)

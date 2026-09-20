"""
c_tests/b_system/a_planning/a_test_project_decomposition.py
=========================================================
Especificação executável de decomposição de projetos em Tasks do AAF.
Valida que o ProjectPlan decompõe a solicitação analítica em tarefas atômicas
com agente designado, capabilities declaradas, dependências e artefatos esperados.
"""
import pytest

from a_platform.b_contracts.f_plan import ProjectPlan
from a_platform.b_contracts.e_task import ProjectTask


def test_project_decomposition_structure():
    """Valida a estrutura de decomposição analítica em pipeline: ingestão -> transformação -> exportação."""
    t1 = ProjectTask(
        task_id="task_ingest",
        name="Ingestão de Dados Brutos",
        assigned_agent="DataAgent",
        capabilities=["data-ingestion"],
        dependencies=[],
        expected_artifacts=["src/ingest.py"],
        commands=["python -m py_compile src/ingest.py"],
    )
    t2 = ProjectTask(
        task_id="task_transform",
        name="Transformação e Limpeza",
        assigned_agent="DataAgent",
        capabilities=["data-cleaning", "data-transformation"],
        dependencies=["task_ingest"],
        expected_artifacts=["src/transform.py"],
        commands=["python -m py_compile src/transform.py"],
    )
    t3 = ProjectTask(
        task_id="task_quality",
        name="Testes de Unidade e Qualidade",
        assigned_agent="TestingAgent",
        capabilities=["dataset-validation"],
        dependencies=["task_transform"],
        expected_artifacts=["tests/test_pipeline.py"],
        commands=["pytest"],
    )

    plan = ProjectPlan(
        project_id="prj_decomp_1",
        domain="analytics",
        tasks=[t1, t2, t3],
    )

    assert len(plan.tasks) == 3
    assert plan.tasks[0].dependencies == []
    assert "task_ingest" in plan.tasks[1].dependencies
    assert "task_transform" in plan.tasks[2].dependencies

    all_caps = plan.get_all_capabilities()
    assert "data-ingestion" in all_caps
    assert "data-cleaning" in all_caps
    assert "data-transformation" in all_caps
    assert "dataset-validation" in all_caps

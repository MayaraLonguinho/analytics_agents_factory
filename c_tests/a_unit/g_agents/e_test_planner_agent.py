"""
c_tests/a_unit/g_agents/e_test_planner_agent.py
=============================================
Especificação executável de PlannerAgent.
Valida decomposição do projeto em DAG de Tasks, atribuição de agentes homologados,
preflight de CommandPolicy e suporte estrito aos domínios analytics e data_engineering.
"""
from unittest.mock import AsyncMock, patch
import pytest

from a_platform.g_agents.d_planner.k_planner_agent import PlannerAgent
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.c_brain.d_domains.a_domain_registry import DomainRegistry
from a_platform.j_llm_gateway.a_interfaces.a_base_provider import LLMResponse


def test_planner_agent_rejects_unsupported_domain():
    """Valida que PlannerAgent rejeita domínios fora de analytics e data_engineering."""
    registry = DomainRegistry()
    planner = PlannerAgent(registry=registry)
    ctx = ExecutionContext(project_id="prj_plan_err", domain="unsupported_game_dev")
    success = planner.generate_plan(ctx)
    assert success is False
    assert ctx.project_plan is None


@pytest.mark.asyncio
async def test_planner_agent_generates_valid_plan(mock_api_keys):
    """Valida a geração de ProjectPlan com tasks, capabilities e agentes atribuídos."""
    registry = DomainRegistry()
    planner = PlannerAgent(registry=registry)
    ctx = ExecutionContext(
        project_id="prj_plan_ok",
        domain="analytics",
        prompt="Criar pipeline de vendas",
    )

    tasks_payload = {
        "tasks": [
            {
                "task_id": "task_1",
                "name": "Ingest Data",
                "description": "Ingest CSV",
                "assigned_agent": "DataAgent",
                "capabilities": ["data-ingestion"],
                "dependencies": [],
                "expected_artifacts": ["ingest.py"],
                "commands": ["python ingest.py"],
                "validators": ["syntax_check"],
            }
        ]
    }

    with patch.object(planner.gateway, "structured_output", new_callable=AsyncMock) as mock_struct:
        mock_struct.return_value = LLMResponse(content=tasks_payload, model="gpt-4o-mini", provider="openai")
        success = await planner._generate_plan_async(ctx)
        assert success is True
        assert ctx.project_plan is not None
        assert len(ctx.project_plan.tasks) == 1
        assert ctx.project_plan.tasks[0].task_id == "task_1"
        assert ctx.project_plan.tasks[0].assigned_agent == "DataAgent"

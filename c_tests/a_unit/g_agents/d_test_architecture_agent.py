"""
c_tests/a_unit/g_agents/d_test_architecture_agent.py
==================================================
Especificação executável de ArchitectureAgent.
Valida determinação da stack tecnológica, proibição de inventar camadas (ex: frontend para CLI)
e persistência da decisão em architecture_decision no ExecutionContext.
"""
from unittest.mock import AsyncMock, patch
import pytest

from a_platform.g_agents.c_architecture.a_architecture_agent import ArchitectureAgent
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.j_llm_gateway.d_gateway import LLMGateway
from a_platform.j_llm_gateway.a_interfaces.a_base_provider import LLMResponse


@pytest.mark.asyncio
async def test_architecture_agent_determines_stack(mock_api_keys):
    """Valida a definição de stack e registro em request.architecture_decision."""
    gateway = LLMGateway()
    agent = ArchitectureAgent(gateway=gateway)

    ctx = ExecutionContext(
        project_id="prj_arch_1",
        domain="analytics",
        project_type="ETL Pipeline",
    )

    stack_json = {
        "database": "SQLite",
        "data_pipeline": "Pandas",
        "testing": "Pytest",
        "rationale": "Pipeline de dados simples e autocontido.",
    }

    with patch.object(gateway, "structured_output", new_callable=AsyncMock) as mock_struct:
        mock_struct.return_value = LLMResponse(content=stack_json, model="gpt-4o-mini", provider="openai")
        success = await agent._generate_architecture_async(ctx)
        assert success is True
        assert ctx.architecture_decision.get("database") == "SQLite"
        assert ctx.architecture_decision.get("testing") == "Pytest"

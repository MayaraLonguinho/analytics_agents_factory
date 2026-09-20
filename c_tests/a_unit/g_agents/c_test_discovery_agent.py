"""
c_tests/a_unit/g_agents/c_test_discovery_agent.py
===============================================
Especificação executável de DiscoveryAgent.
Valida extração de requisitos, orçamento de perguntas (budget <= 5),
transição para NEEDS_INPUT quando falta informação crítica e proibição de inventar dados.
"""
from unittest.mock import AsyncMock, patch
import pytest

from a_platform.g_agents.b_discovery.a_discovery_agent import DiscoveryAgent, DiscoveryStatus
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.j_llm_gateway.a_interfaces.a_base_provider import LLMResponse


@pytest.mark.asyncio
async def test_discovery_agent_budget_exhaustion(mock_api_keys):
    """Valida que o agente de discovery não excede o orçamento de 5 perguntas."""
    agent = DiscoveryAgent()
    ctx = ExecutionContext(project_id="prj_disc_1", prompt="Build ETL")
    ctx.discovery_data["question_count"] = 5  # Orçamento esgotado

    status = await agent.run(ctx)
    assert status == DiscoveryStatus.COMPLETE


@pytest.mark.asyncio
async def test_discovery_agent_needs_input_when_missing_info(mock_api_keys):
    """Valida transição para NEEDS_INPUT quando informação indispensável está ausente."""
    agent = DiscoveryAgent()
    ctx = ExecutionContext(project_id="prj_disc_2", prompt="Build analytics pipeline")
    ctx.discovery_data["question_count"] = 0

    llm_payload = (
        '{"project_type": "Pipeline", "business_context": "Vendas", "domain": "analytics", '
        '"missing_info_question": "Qual o destino do pipeline (banco, arquivo, S3)?", '
        '"decisions": [], "assumed_defaults": []}'
    )
    with patch.object(agent.gateway, "generate", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = LLMResponse(content=llm_payload, model="gpt-4o-mini", provider="openai")
        status = await agent.run(ctx)
        assert status == DiscoveryStatus.NEEDS_INPUT
        assert ctx.discovery_data.get("pending_question") is not None

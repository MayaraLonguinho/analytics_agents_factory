"""
c_tests/a_unit/f_llm_gateway/c_test_system_prompt.py
==================================================
Especificação executável de preservação do system_prompt no LLMGateway.
Garante que instruções de sistema e guardrails de papéis não sejam descartados
ou truncados durante a chamada ao provedor.
"""
from unittest.mock import AsyncMock, patch
import pytest

from a_platform.j_llm_gateway.d_gateway import LLMGateway
from a_platform.j_llm_gateway.a_interfaces.a_base_provider import LLMResponse


@pytest.mark.asyncio
async def test_gateway_preserves_system_prompt(mock_api_keys):
    """Valida que o system_prompt é fielmente repassado ao provedor subjacente."""
    gateway = LLMGateway()
    provider = gateway.provider_registry.get_provider("openai")

    if provider:
        with patch.object(provider, "generate", new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = LLMResponse(content="OK", model="gpt-4o-mini", provider="openai")
            system_instruction = "Você é um engenheiro sênior de dados."
            user_msg = "Gere um script de ingestão."

            await gateway.generate(prompt=user_msg, system_prompt=system_instruction)

            mock_gen.assert_called_once()
            called_kwargs = mock_gen.call_args.kwargs
            assert called_kwargs.get("system_prompt") == system_instruction

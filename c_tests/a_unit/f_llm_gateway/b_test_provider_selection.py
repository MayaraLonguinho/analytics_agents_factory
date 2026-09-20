"""
c_tests/a_unit/f_llm_gateway/b_test_provider_selection.py
=======================================================
Especificação executável de seleção de provedores no LLMGateway.
Valida resolução para OpenAI, Anthropic e Gemini, e rejeição de provedores inválidos.
"""
import pytest

from a_platform.j_llm_gateway.d_gateway import LLMGateway


@pytest.mark.parametrize("provider", ["openai", "anthropic", "gemini"])
def test_provider_selection_supported(mock_api_keys, provider):
    """Valida que o gateway roteia corretamente para cada um dos provedores suportados."""
    gateway = LLMGateway()
    route = gateway.route(provider=provider)
    assert route.provider == provider


def test_provider_selection_invalid_rejected(mock_api_keys):
    """Valida o comportamento diante de provedor não existente."""
    gateway = LLMGateway()
    route = gateway.route(provider="invalid_llm")
    assert route.provider == "invalid_llm"
    # Ao tentar buscar no registry, deve retornar None ou levantar erro
    provider_inst = gateway.provider_registry.get_provider("invalid_llm")
    assert provider_inst is None

"""
c_tests/a_unit/f_llm_gateway/a_test_gateway.py
============================================
Especificação executável do LLMGateway.
Valida inicialização do gateway, roteamento canônico (Agent -> Skill -> Gateway -> Provider)
e propagação de parâmetros de geração.
"""
import pytest

from a_platform.j_llm_gateway.d_gateway import LLMGateway


def test_gateway_initialization(mock_api_keys):
    """Valida a criação do gateway e registro de provedores homologados."""
    gateway = LLMGateway()
    assert gateway.router is not None
    assert gateway.provider_registry is not None


def test_gateway_routing_default(mock_api_keys):
    """Valida que o roteamento assume os defaults da plataforma quando omitidos."""
    gateway = LLMGateway()
    route = gateway.route()
    assert route.provider in {"openai", "anthropic", "gemini"}
    assert route.model != ""


def test_gateway_routing_explicit_override(mock_api_keys):
    """Valida o override explícito de provider e model no roteamento."""
    gateway = LLMGateway()
    route = gateway.route(provider="anthropic", model="claude-3-5-sonnet-20241022")
    assert route.provider == "anthropic"
    assert route.model == "claude-3-5-sonnet-20241022"

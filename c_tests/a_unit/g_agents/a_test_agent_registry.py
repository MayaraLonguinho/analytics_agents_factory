"""
c_tests/a_unit/g_agents/a_test_agent_registry.py
==============================================
Especificação executável de AgentRegistry.
Valida o catálogo de contratos de agentes, validação de responsabilidade e permissões.
"""
import pytest

from a_platform.g_agents.o_registry.a_registry import AgentRegistry


def test_agent_registry_initialization():
    """Valida a inicialização do catálogo de agentes."""
    registry = AgentRegistry()
    agents = registry.list_agents()
    assert isinstance(agents, list)


def test_agent_registry_query_by_id():
    """Valida a consulta de contratos de agentes por identificador."""
    registry = AgentRegistry()
    # Se houver agentes declarados no YAML, valida formato
    if registry.agents:
        first_id = next(iter(registry.agents.keys()))
        agent = registry.get_agent(first_id)
        assert agent is not None
        assert agent.agent_id == first_id

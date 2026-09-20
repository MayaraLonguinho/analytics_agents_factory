"""
c_tests/a_unit/g_agents/b_test_agent_factory.py
=============================================
Especificação executável de AgentFactory.
Valida instanciação concreta de agentes especializados (DataAgent, AnalyticsAgent, TestingAgent)
com injeção de gateway, MCP e skills.
"""
import pytest

from a_platform.g_agents.n_factory.a_agent_factory import AgentFactory
from a_platform.g_agents.a_base.a_base_agent import BaseAgent
from a_platform.g_agents.e_data.a_data_agent import DataAgent
from a_platform.g_agents.g_analytics.a_analytics_agent import AnalyticsAgent
from a_platform.g_agents.h_testing.a_testing_agent import TestingAgent


def test_agent_factory_creates_data_agent(mock_api_keys):
    """Valida a resolução e instanciação de DataAgent."""
    factory = AgentFactory()
    agent = factory.get_agent("DataAgent")
    assert isinstance(agent, DataAgent)
    assert isinstance(agent, BaseAgent)


def test_agent_factory_creates_analytics_agent(mock_api_keys):
    """Valida a resolução e instanciação de AnalyticsAgent."""
    factory = AgentFactory()
    agent = factory.get_agent("AnalyticsAgent")
    assert isinstance(agent, AnalyticsAgent)


def test_agent_factory_creates_testing_agent(mock_api_keys):
    """Valida a resolução e instanciação de TestingAgent."""
    factory = AgentFactory()
    agent = factory.get_agent("TestingAgent")
    assert isinstance(agent, TestingAgent)


def test_agent_factory_caching(mock_api_keys):
    """Valida que instâncias de agentes são reutilizadas a partir do cache."""
    factory = AgentFactory()
    a1 = factory.get_agent("DataAgent")
    a2 = factory.get_agent("DataAgent")
    assert a1 is a2

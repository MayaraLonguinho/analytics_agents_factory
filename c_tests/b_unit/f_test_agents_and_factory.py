import os
os.environ['OPENAI_API_KEY'] = 'sk-dummy'
os.environ['ANTHROPIC_API_KEY'] = 'sk-dummy'
os.environ['GEMINI_API_KEY'] = 'sk-dummy'

from a_platform.d_agents.m_agent_factory.a_agent_factory import AgentFactory
from a_platform.d_agents.p_base.a_base_agent import BaseAgent

def test_agent_factory_creation():
    factory = AgentFactory()
    agent = factory.get_agent("DataAgent")
    assert isinstance(agent, BaseAgent)

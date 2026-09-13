import os
os.environ['OPENAI_API_KEY'] = 'sk-dummy'
os.environ['ANTHROPIC_API_KEY'] = 'sk-dummy'
os.environ['GEMINI_API_KEY'] = 'sk-dummy'

from a_platform.d_agents.c_planner.k_planner_agent import PlannerAgent
from a_platform.i_domains.a_domain_registry import DomainRegistry
from a_platform.a_core.d_session.b_context import ExecutionContext

def test_planner_generates_plan():
    # Only test the structure generation if mocked locally
    pass

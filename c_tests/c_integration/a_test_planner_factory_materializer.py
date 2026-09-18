import os
os.environ['OPENAI_API_KEY'] = 'sk-dummy'
os.environ['ANTHROPIC_API_KEY'] = 'sk-dummy'
os.environ['GEMINI_API_KEY'] = 'sk-dummy'

from a_platform.g_agents.d_planner.k_planner_agent import PlannerAgent
from a_platform.c_brain.a_domain_registry import DomainRegistry
from a_platform.b_contracts.e_execution_context import ExecutionContext

def test_planner_generates_plan():
    # Only test the structure generation if mocked locally
    pass

import os

files_to_create = {
    "c_agents/c_planner_agent/__init__.py": "",
    "c_agents/c_planner_agent/prompt_templates/__init__.py": "",
    "c_agents/c_planner_agent/prompt_templates/planner_prompts.py": """\
PLANNER_SYSTEM_PROMPT = "You are a Technical Project Planner. Decompose architecture into a sequence of tasks."
""",
    "c_agents/c_planner_agent/task_decomposer.py": """\
from typing import List

class TaskDecomposer:
    def decompose(self, domain: str) -> List[str]:
        # Simple topological sort DAG representation
        return ["db_setup", "etl_pipeline", "backend_api", "frontend_dashboard", "devops_infra", "qa_tests"]
""",
    "c_agents/c_planner_agent/planner_agent.py": """\
from typing import Optional
from a_platform.a_core.b_domain.project_plan import ProjectPlan
from a_platform.f_llm_gateway.gateway import LLMGateway
from c_agents.c_planner_agent.task_decomposer import TaskDecomposer

class PlannerAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()
        self.decomposer = TaskDecomposer()

    async def execute(self, plan: ProjectPlan) -> ProjectPlan:
        tasks = self.decomposer.decompose(plan.domain)
        plan.tasks = tasks
        return plan
""",
    "c_agents/d_etl_agent/__init__.py": "",
    "c_agents/d_etl_agent/prompt_templates/__init__.py": "",
    "c_agents/d_etl_agent/prompt_templates/etl_prompts.py": """\
ETL_PROMPT = "Generate an ETL script"
""",
    "c_agents/d_etl_agent/etl_agent.py": """\
from typing import Optional
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.f_llm_gateway.gateway import LLMGateway

class ETLAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    async def execute(self, task_name: str) -> Artifact:
        return Artifact(name="etl_script", path="etl.py", content="# ETL pipeline")
""",
    "c_agents/e_db_agent/__init__.py": "",
    "c_agents/e_db_agent/prompt_templates/__init__.py": "",
    "c_agents/e_db_agent/prompt_templates/db_prompts.py": """\
DB_PROMPT = "Generate a DDL script"
""",
    "c_agents/e_db_agent/db_agent.py": """\
from typing import Optional
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.f_llm_gateway.gateway import LLMGateway

class DBAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    async def execute(self, task_name: str) -> Artifact:
        return Artifact(name="db_schema", path="schema.sql", content="CREATE TABLE ...")
""",
    "c_agents/f_backend_agent/__init__.py": "",
    "c_agents/f_backend_agent/prompt_templates/__init__.py": "",
    "c_agents/f_backend_agent/prompt_templates/backend_prompts.py": """\
BACKEND_PROMPT = "Generate a FastAPI app"
""",
    "c_agents/f_backend_agent/backend_agent.py": """\
from typing import Optional
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.f_llm_gateway.gateway import LLMGateway

class BackendAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    async def execute(self, task_name: str) -> Artifact:
        return Artifact(name="main_api", path="main.py", content="from fastapi import FastAPI")
""",
    "c_agents/g_frontend_agent/__init__.py": "",
    "c_agents/g_frontend_agent/prompt_templates/__init__.py": "",
    "c_agents/g_frontend_agent/prompt_templates/frontend_prompts.py": """\
FRONTEND_PROMPT = "Generate a dashboard"
""",
    "c_agents/g_frontend_agent/frontend_agent.py": """\
from typing import Optional
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.f_llm_gateway.gateway import LLMGateway

class FrontendAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    async def execute(self, task_name: str) -> Artifact:
        return Artifact(name="dashboard", path="app.py", content="import streamlit as st")
""",
    "c_agents/h_devops_agent/__init__.py": "",
    "c_agents/h_devops_agent/prompt_templates/__init__.py": "",
    "c_agents/h_devops_agent/prompt_templates/devops_prompts.py": """\
DEVOPS_PROMPT = "Generate Docker files"
""",
    "c_agents/h_devops_agent/devops_agent.py": """\
from typing import Optional
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.f_llm_gateway.gateway import LLMGateway

class DevOpsAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    async def execute(self, task_name: str) -> Artifact:
        return Artifact(name="dockerfile", path="Dockerfile", content="FROM python:3.9")
""",
    "c_agents/i_qa_agent/__init__.py": "",
    "c_agents/i_qa_agent/prompt_templates/__init__.py": "",
    "c_agents/i_qa_agent/prompt_templates/qa_prompts.py": """\
QA_PROMPT = "Generate test cases"
""",
    "c_agents/i_qa_agent/qa_agent.py": """\
from typing import Optional
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.f_llm_gateway.gateway import LLMGateway

class QAAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    async def execute(self, task_name: str) -> Artifact:
        return Artifact(name="tests", path="test_main.py", content="def test_app(): pass")
""",
    "c_tests/unit/test_planner_agent.py": """\
import pytest
from c_agents.c_planner_agent.planner_agent import PlannerAgent
from a_platform.a_core.b_domain.project_plan import ProjectPlan

@pytest.mark.asyncio
async def test_planner_agent_execute():
    agent = PlannerAgent()
    plan = ProjectPlan(project_id="test", name="test", domain="generic")
    result = await agent.execute(plan)
    assert len(result.tasks) == 6
    assert result.tasks[0] == "db_setup"
    assert result.tasks[-1] == "qa_tests"
""",
    "c_tests/unit/test_specialist_agents.py": """\
import pytest
from c_agents.d_etl_agent.etl_agent import ETLAgent
from c_agents.e_db_agent.db_agent import DBAgent
from c_agents.f_backend_agent.backend_agent import BackendAgent
from c_agents.g_frontend_agent.frontend_agent import FrontendAgent
from c_agents.h_devops_agent.devops_agent import DevOpsAgent
from c_agents.i_qa_agent.qa_agent import QAAgent

@pytest.mark.asyncio
async def test_all_specialists():
    agents = [
        ETLAgent(), DBAgent(), BackendAgent(),
        FrontendAgent(), DevOpsAgent(), QAAgent()
    ]
    for agent in agents:
        artifact = await agent.execute("test_task")
        assert artifact.path
        assert artifact.content
"""
}

for path, content in files_to_create.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


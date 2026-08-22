import pytest
from a_platform.c_agents.e_data.etl_agent import ETLAgent
from a_platform.c_agents.f_database.db_agent import DBAgent
from a_platform.c_agents.g_backend.backend_agent import BackendAgent
from a_platform.c_agents.h_frontend.frontend_agent import FrontendAgent
from a_platform.c_agents.j_infrastructure.devops_agent import DevOpsAgent
from a_platform.c_agents.k_testing.qa_agent import QAAgent

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

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

import pytest
from c_agents.a_discovery_agent.discovery_agent import DiscoveryAgent
from a_platform.a_core.b_domain.project_request import ProjectRequest

@pytest.mark.asyncio
async def test_discovery_agent_execute():
    agent = DiscoveryAgent()
    request = ProjectRequest.from_raw("Build a finance dashboard", domain="finance")
    result = await agent.execute(request)
    assert result.domain == "finance"
    assert result.request == "Build a finance dashboard"

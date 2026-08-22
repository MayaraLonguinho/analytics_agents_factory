import pytest
from a_platform.c_agents.c_architecture.architecture_agent import ArchitectureAgent
from a_platform.a_core.b_domain.discovery import DiscoveryResult

@pytest.mark.asyncio
async def test_architecture_agent_execute():
    agent = ArchitectureAgent()
    discovery = DiscoveryResult(
        project_objective="Test",
        domain="finance",
        request="Test request"
    )
    plan = await agent.execute(discovery)
    assert "Fact: fact_transactions" in plan.metadata.get("backend_architecture", "")

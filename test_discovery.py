import asyncio
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.d_agents.b_discovery.discovery_agent import DiscoveryAgent

async def test():
    agent = DiscoveryAgent()
    req = ProjectRequest(prompt="Quero um dashboard de e-commerce e CRM")
    res = agent.run_discovery(req)
    print("Test 1 (ecommerce):")
    print("Domain:", req.discovery_data.get("domain"))
    print("Business Context:", req.discovery_data.get("business_context"))
    
    req2 = ProjectRequest(prompt="Pipeline ETL para dados de HR e finance")
    res2 = agent.run_discovery(req2)
    print("Test 2 (finance/hr):")
    print("Domain:", req2.discovery_data.get("domain"))
    print("Business Context:", req2.discovery_data.get("business_context"))

asyncio.run(test())

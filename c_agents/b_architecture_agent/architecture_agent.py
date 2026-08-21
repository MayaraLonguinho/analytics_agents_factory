from typing import Optional
from a_platform.a_core.b_domain.discovery import DiscoveryResult
from a_platform.a_core.b_domain.project_plan import ProjectPlan
from a_platform.f_llm_gateway.gateway import LLMGateway
from c_agents.b_architecture_agent.schema_designer import SchemaDesigner

class ArchitectureAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()
        self.schema_designer = SchemaDesigner()

    async def execute(self, discovery: DiscoveryResult) -> ProjectPlan:
        schema = self.schema_designer.design_star_schema(discovery.domain or "generic")
        plan = ProjectPlan(
            project_id="arch-plan-001",
            name="Architecture Plan",
            domain=discovery.domain or "generic",
            metadata={
                "backend_architecture": f"Fact: {schema['fact']}",
                "frontend_architecture": "Dashboard",
                "database_architecture": "Star Schema"
            }
        )
        return plan

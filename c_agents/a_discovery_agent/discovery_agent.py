from typing import Optional
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.discovery import DiscoveryResult
from a_platform.f_llm_gateway.gateway import LLMGateway
from c_agents.a_discovery_agent.prompt_templates.discovery_prompts import DISCOVERY_SYSTEM_PROMPT, DISCOVERY_USER_PROMPT

class DiscoveryAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    async def execute(self, request: ProjectRequest) -> DiscoveryResult:
        # Simplistic discovery execution
        prompt = DISCOVERY_USER_PROMPT.format(request=request.request)
        result_text = await self.gateway.generate(prompt, complexity="low", system_prompt=DISCOVERY_SYSTEM_PROMPT)
        
        result = DiscoveryResult(
            project_objective="Extracted objective based on: " + request.request,
            domain=request.domain,
            request=request.request,
            source=request.source,
            dataset_source=request.dataset_source
        )
        return result

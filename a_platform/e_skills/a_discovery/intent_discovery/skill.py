import logging
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill, ParameterDefinition
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class IntentDiscoverySkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="discover-intent",
            name="Intent Discovery Skill",
            input_schema=[
                ParameterDefinition(name="request_text", data_type="string", required=True),
            ],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        req_text = context["request_text"]
        system_prompt = "Você é um especialista em análise de requisitos para projetos de dados. Extraia os objetivos e requisitos principais."
        user_prompt = f"Solicitação: {req_text}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        result = {"intent.json": resp.content or "{}"}
        self.validate_output(result)
        return result

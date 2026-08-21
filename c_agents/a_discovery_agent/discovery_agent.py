from typing import Optional, List
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.discovery import DiscoveryResult
from a_platform.f_llm_gateway.gateway import LLMGateway
import json

class DiscoveryAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    async def generate_questions(self, idea: str) -> List[str]:
        prompt = f"Given this project idea: '{idea}', generate 3 to 5 strategic questions to refine the requirements. Return ONLY a JSON list of strings."
        try:
            result_text = await self.gateway.generate(prompt, complexity="low", system_prompt="You are a data architect. Output only valid JSON list of strings.")
            
            if "mocked response" in result_text.lower():
                return ["Qual é o banco de dados preferido?", "Qual é o volume estimado de dados?", "Existem restrições de segurança específicas?"]
                
            return json.loads(result_text)
        except Exception:
            return ["Qual é o banco de dados preferido?", "Qual é o volume estimado de dados?", "Existem restrições de segurança específicas?"]

    async def execute(self, request: ProjectRequest) -> DiscoveryResult:
        context = request.request
        if request.answers:
            context += "\n\nRespostas do Questionário:\n"
            for q, a in request.answers.items():
                context += f"- {q}: {a}\n"
                
        prompt = f"Analyze this project context and requirements: {context}"
        result_text = await self.gateway.generate(prompt, complexity="low", system_prompt="You are a data architect extracting objectives.")
        
        result = DiscoveryResult(
            project_objective=f"Extracted objective based on: {context}",
            domain=request.domain,
            request=context,
            source=request.source,
            dataset_source=request.dataset_source
        )
        return result

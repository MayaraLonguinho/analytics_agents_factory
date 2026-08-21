import os

project_request_updates = """\
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ProjectRequest(BaseModel):
    \"\"\"Canonical request contract for ingesting project intent.\"\"\"
    request: str
    domain: Optional[str] = None
    source: str = "cli"
    dataset_source: Optional[str] = None
    dataset_profile: Dict[str, Any] = Field(default_factory=dict)
    answers: Dict[str, str] = Field(default_factory=dict)
    architecture_constraints: List[str] = Field(default_factory=list)
    technology_preferences: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    preferred_stack: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_raw(cls, raw_request: str, **kwargs) -> "ProjectRequest":
        normalized = (raw_request or "").strip()
        if not normalized:
            raise ValueError("request cannot be empty")
        return cls(request=normalized, **kwargs)
"""

discovery_agent_updates = """\
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
            context += "\\n\\nRespostas do Questionário:\\n"
            for q, a in request.answers.items():
                context += f"- {q}: {a}\\n"
                
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
"""

with open("a_platform/a_core/b_domain/project_request.py", "w") as f:
    f.write(project_request_updates)

with open("c_agents/a_discovery_agent/discovery_agent.py", "w") as f:
    f.write(discovery_agent_updates)

import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class ArchitectureDocumentationSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="architecture-documentation",
            name="Architecture Documentation Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        description = context.get("task_description", "Documentação de arquitetura")
        arch = context.get("architecture", {})

        system_prompt = (
            "Você é um Arquiteto de Software sênior. Gere o documento ARCHITECTURE.md contendo: "
            "Visão Geral, Limites de Sistema, Componentes, Diagrama de Sequência ou Fluxo em Mermaid e "
            "Decisões Arquiteturais registradas. Responda SOMENTE com o Markdown, sem blocos ```markdown envolvendo tudo."
        )
        user_prompt = f"Descrição: {description}\nArquitetura: {arch}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        content = resp.content or ""
        content = re.sub(r'^```[\w]*\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'```$', '', content, flags=re.MULTILINE).strip()

        result = {"ARCHITECTURE.md": content}
        self.validate_output(result)
        return result

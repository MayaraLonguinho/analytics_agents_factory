import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class TechnicalDocumentationSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="technical-documentation",
            name="Technical Documentation Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        description = context.get("task_description", "Documentação técnica do projeto")
        plan = context.get("project_plan", {})
        arch = context.get("architecture", {})

        system_prompt = (
            "Você é um Staff Technical Writer e Arquiteto de Software. "
            "Gere uma documentação técnica impecável em Markdown cobrindo objetivo, arquitetura, "
            "fluxo de dados, dicionário de tabelas e passos de operação. "
            "Responda SOMENTE com o texto em Markdown, sem markdown code block (```markdown) envolvendo o arquivo todo."
        )
        user_prompt = f"Descrição: {description}\nArquitetura: {arch}\nPlano: {plan}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        content = resp.content or ""
        content = re.sub(r'^```[\w]*\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'```$', '', content, flags=re.MULTILINE).strip()

        result = {"TECHNICAL_DOCS.md": content}
        self.validate_output(result)
        return result

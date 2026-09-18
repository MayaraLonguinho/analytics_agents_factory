import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class ApiDesignSkill(BaseSkill):
    def __init__(self):
        super().__init__()
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)

        domain = context["domain"]
        description = context.get("task_description", "")
        project_plan = context.get("project_plan", {})

        logger.info(f"[ApiDesignSkill] Gerando swagger para {domain} usando LLM")

        system_prompt = (
            "Você é um engenheiro de software arquiteto de APIs. "
            "Sua tarefa é gerar a especificação OpenAPI 3.0 (Swagger) em formato YAML limpo e completo. "
            "Responda SOMENTE com o YAML. Não use markdown formatting (```yaml) na resposta."
        )
        user_prompt = (
            f"Domain: {domain}\nDescrição: {description}\n"
            f"Plan: {project_plan}\n\nGere a spec OpenAPI (swagger.yaml)."
        )

        llm_response = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)

        if not llm_response.content:
            msg = "[ApiDesignSkill] LLM retornou conteúdo vazio."
            logger.error(msg)
            raise ValueError(msg)

        code_text = llm_response.content
        code_text = re.sub(r'^```[\w]*\n', '', code_text, flags=re.MULTILINE)
        code_text = re.sub(r'```$', '', code_text, flags=re.MULTILINE).strip()

        result = {"swagger.yaml": code_text}
        self.validate_output(result)
        return result

import logging
import re
from typing import Dict, Any
from a_platform.e_skills.skill_contract import BaseSkill, CORE_SKILL_CONTRACTS
from a_platform.g_llm_gateway.gateway import LLMGateway

logger = logging.getLogger(__name__)

class ApiDesignSkill(BaseSkill):
    def __init__(self):
        super().__init__(contract=CORE_SKILL_CONTRACTS["api_design"])
        self.llm = LLMGateway()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        
        domain = context["domain"]
        description = context.get("task_description", "")
        project_plan = context.get("project_plan", {})
        
        logger.info(f"[ApiDesignSkill] Gerando swagger para {domain} usando LLM")
        
        system_prompt = (
            "Você é um engenheiro de software arquiteto de APIs. "
            "Sua tarefa é gerar a especificação OpenAPI 3.0 (Swagger) em formato YAML limpo e completo, "
            "baseado nos requisitos da API para o domínio especificado. "
            "Responda SOMENTE com o YAML. Não inclua texto ao redor. Não use markdown formatting (```yaml) na resposta."
        )

        user_prompt = f"Domain: {domain}\nDescrição: {description}\nPlan: {project_plan}\n\nGere a spec OpenAPI (swagger.yaml)."

        llm_response = self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        if llm_response["success"]:
            code_text = llm_response["text"]
            code_text = re.sub(r'^```[\w]*\n', '', code_text, flags=re.MULTILINE)
            code_text = re.sub(r'```$', '', code_text, flags=re.MULTILINE).strip()
        else:
            logger.error(f"[ApiDesignSkill] Falha LLM: {llm_response.get('error')}")
            code_text = f"# LLM Generation Failed: {llm_response.get('error')}\nopenapi: 3.0.0\ninfo:\n  title: {domain} API\n  version: 1.0.0"
        
        result = {
            "swagger.yaml": code_text
        }
        
        self.validate_output(result)
        return result

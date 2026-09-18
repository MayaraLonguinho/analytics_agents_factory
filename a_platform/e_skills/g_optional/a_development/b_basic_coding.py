import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.i_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class BasicCodingSkill(BaseSkill):
    def __init__(self):
        super().__init__()
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)

        script_name = context["script_name"]
        description = context.get("task_description", "")
        project_plan = context.get("project_plan", {})
        discovery = context.get("discovery_requirements", {})
        architecture = context.get("architecture_context", {})
        rules = context.get("brain_rules", [])

        logger.info(f"[BasicCodingSkill] Gerando código para {script_name} usando LLM")

        system_prompt = (
            "Você é um engenheiro de software sênior. Gere código limpo, documentado, tipado e funcional. "
            "Responda SOMENTE com o código do arquivo solicitado. Não use markdown formatting (```python) na resposta."
        )
        user_prompt = (
            f"Gere o arquivo {script_name} considerando:\n"
            f"Descrição: {description}\nRegras: {rules}\n"
            f"Arquitetura: {architecture}\nDiscovery: {discovery}\nPlan: {project_plan}"
        )

        llm_response = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)

        if not llm_response.content:
            msg = f"[BasicCodingSkill] LLM retornou conteúdo vazio para {script_name}."
            logger.error(msg)
            raise ValueError(msg)

        code_text = llm_response.content
        # Clean up markdown if model ignored the instruction
        code_text = re.sub(r'^```[\w]*\n', '', code_text, flags=re.MULTILINE)
        code_text = re.sub(r'```$', '', code_text, flags=re.MULTILINE).strip()

        result = {script_name: code_text}
        self.validate_output(result)
        return result

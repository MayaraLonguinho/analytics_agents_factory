import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class DependencyQualitySkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="dependency-quality",
            name="Dependency Quality Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        description = context.get("task_description", "Geração de requirements.txt mínimo")
        plan = context.get("project_plan", {})
        arch = context.get("architecture", {})

        system_prompt = (
            "Você é um engenheiro de software especialista em packaging Python. "
            "Gere o arquivo requirements.txt com as dependências estritamente necessárias "
            "(ex: pandas>=2.0.0, pytest>=7.0.0), devidamente pinadas e sem bibliotecas supérfluas. "
            "Responda SOMENTE com o conteúdo do requirements.txt."
        )
        user_prompt = f"Descrição: {description}\nArquitetura: {arch}\nPlano: {plan}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        content = resp.content or ""
        content = re.sub(r'^```[\w]*\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'```$', '', content, flags=re.MULTILINE).strip()

        result = {"requirements.txt": content}
        self.validate_output(result)
        return result

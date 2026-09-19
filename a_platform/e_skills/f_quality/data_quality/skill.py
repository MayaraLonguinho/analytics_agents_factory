import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class DataQualitySkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="data-quality",
            name="Data Quality Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        description = context.get("task_description", "Validação de qualidade de dados")

        system_prompt = (
            "Você é um engenheiro de QA e Data Quality. Gere um script Python de teste de dados "
            "com asserções claras sobre o banco ou tabelas finais: checagem de linhas não-vazias, "
            "completude de campos essenciais, tipos numéricos válidos e unicidade. "
            "Responda SOMENTE com o código Python, sem markdown formatting (```python)."
        )
        user_prompt = f"Descrição: {description}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        code = resp.content or ""
        code = re.sub(r'^```[\w]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'```$', '', code, flags=re.MULTILINE).strip()

        result = {"data_quality.py": code}
        self.validate_output(result)
        return result

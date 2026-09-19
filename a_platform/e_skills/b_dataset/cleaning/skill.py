import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class DataCleaningSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="data-cleaning",
            name="Data Cleaning Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        description = context.get("task_description", "Limpeza e sanitização de dados")
        profile = context.get("dataset_profile", {})

        system_prompt = (
            "Você é um engenheiro de dados sênior especializado em limpeza e qualidade de dados. "
            "Gere uma função/módulo Python limpo e documentado que execute a higienização dos dados: "
            "remoção de duplicatas, padronização de strings, conversão de tipos e tratamento de nulos. "
            "Responda SOMENTE com o código Python, sem markdown formatting (```python)."
        )
        user_prompt = f"Descrição: {description}\nPerfil do Dataset: {profile}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        code = resp.content or ""
        code = re.sub(r'^```[\w]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'```$', '', code, flags=re.MULTILINE).strip()

        result = {"cleaner.py": code}
        self.validate_output(result)
        return result

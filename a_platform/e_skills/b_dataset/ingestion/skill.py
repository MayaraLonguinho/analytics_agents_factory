import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill, ParameterDefinition
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class DataIngestionSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="data-ingestion",
            name="Data Ingestion Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        source = context.get("dataset_path", "data.csv")
        description = context.get("task_description", "Ingestão de dados brutos")

        system_prompt = (
            "Você é um engenheiro de dados sênior especializado em ingestão de dados. "
            "Gere um script Python tipado e limpo com função de ingestão que trate encodings, "
            "valide existência do arquivo e carregue os dados de forma eficiente. "
            "Responda SOMENTE com o código Python, sem markdown formatting (```python)."
        )
        user_prompt = f"Fonte: {source}\nDescrição: {description}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        code = resp.content or ""
        code = re.sub(r'^```[\w]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'```$', '', code, flags=re.MULTILINE).strip()

        result = {"ingestion.py": code}
        self.validate_output(result)
        return result

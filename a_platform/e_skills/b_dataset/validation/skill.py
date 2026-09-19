import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class DatasetValidationSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="dataset-validation",
            name="Dataset Validation Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        schema = context.get("schema_definition", "")
        description = context.get("task_description", "Validação do dataset de entrada")

        system_prompt = (
            "Você é um engenheiro de qualidade de dados. Gere um script Python de validação de dados "
            "que verifique colunas esperadas, tipos de dados, completude de chaves e conformidade de schemas. "
            "Responda SOMENTE com o código Python, sem markdown formatting (```python)."
        )
        user_prompt = f"Schema esperado: {schema}\nDescrição: {description}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        code = resp.content or ""
        code = re.sub(r'^```[\w]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'```$', '', code, flags=re.MULTILINE).strip()

        result = {"dataset_validator.py": code}
        self.validate_output(result)
        return result

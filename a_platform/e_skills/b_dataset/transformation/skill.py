import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class DataTransformationSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="data-transformation",
            name="Data Transformation Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        description = context.get("task_description", "Transformação de dados")
        schema = context.get("schema_definition", "")

        system_prompt = (
            "Você é um especialista em transformação de dados com Pandas/Python. "
            "Gere uma função de transformação limpa e tipada para converter e alinhar dados ao schema esperado. "
            "Responda SOMENTE com o código Python, sem markdown formatting (```python)."
        )
        user_prompt = f"Descrição: {description}\nSchema: {schema}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        code = resp.content or ""
        code = re.sub(r'^```[\w]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'```$', '', code, flags=re.MULTILINE).strip()

        result = {"transformation.py": code}
        self.validate_output(result)
        return result

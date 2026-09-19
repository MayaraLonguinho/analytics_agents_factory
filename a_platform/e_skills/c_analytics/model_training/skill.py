import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class ModelTrainingSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="model-training",
            name="Model Training Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        description = context.get("task_description", "Treinamento de modelo")

        system_prompt = (
            "Você é um engenheiro de Machine Learning sênior. Gere um script Python limpo e reprodutível "
            "com scikit-learn para treino de modelo com split, validação cruzada e persistência (joblib). "
            "Responda SOMENTE com o código Python, sem markdown formatting (```python)."
        )
        user_prompt = f"Descrição: {description}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        code = resp.content or ""
        code = re.sub(r'^```[\w]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'```$', '', code, flags=re.MULTILINE).strip()

        result = {"train.py": code}
        self.validate_output(result)
        return result

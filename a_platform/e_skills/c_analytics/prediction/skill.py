import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class PredictionSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="prediction",
            name="Prediction Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        description = context.get("task_description", "Predição e inferência com modelo de ML")

        system_prompt = (
            "Você é um engenheiro de Machine Learning sênior. Gere um script Python de predição "
            "que carregue o modelo treinado, leia novos registros, aplique o pré-processamento e "
            "gere previsões estruturadas salvando em arquivo ou exibindo na saída. "
            "Responda SOMENTE com o código Python, sem markdown formatting (```python)."
        )
        user_prompt = f"Descrição: {description}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        code = resp.content or ""
        code = re.sub(r'^```[\w]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'```$', '', code, flags=re.MULTILINE).strip()

        result = {"predict.py": code}
        self.validate_output(result)
        return result

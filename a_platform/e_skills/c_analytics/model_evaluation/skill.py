import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class ModelEvaluationSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="model-evaluation",
            name="Model Evaluation Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        description = context.get("task_description", "Avaliação de modelo de ML")

        system_prompt = (
            "Você é um engenheiro de Machine Learning sênior. Gere um script Python com scikit-learn "
            "que carregue o modelo treinado e compute métricas completas de validação (classification_report, "
            "confusion_matrix, R2, RMSE etc.) exibindo um resumo claro no terminal. "
            "Responda SOMENTE com o código Python, sem markdown formatting (```python)."
        )
        user_prompt = f"Descrição: {description}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        code = resp.content or ""
        code = re.sub(r'^```[\w]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'```$', '', code, flags=re.MULTILINE).strip()

        result = {"evaluate.py": code}
        self.validate_output(result)
        return result

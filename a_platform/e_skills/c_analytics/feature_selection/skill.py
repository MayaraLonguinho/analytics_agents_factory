import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class FeatureSelectionSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="feature-selection",
            name="Feature Selection Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        description = context.get("task_description", "Seleção de features")

        system_prompt = (
            "Você é um cientista de dados especialista em feature selection. "
            "Gere um script Python usando scikit-learn para ranqueamento e seleção de variáveis "
            "(SelectKBest, RFE ou Feature Importance de Random Forest). "
            "Responda SOMENTE com o código Python, sem markdown formatting (```python)."
        )
        user_prompt = f"Descrição: {description}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        code = resp.content or ""
        code = re.sub(r'^```[\w]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'```$', '', code, flags=re.MULTILINE).strip()

        result = {"feature_selection.py": code}
        self.validate_output(result)
        return result

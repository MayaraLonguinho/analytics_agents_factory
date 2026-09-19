import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class DataVisualizationSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="data-visualization",
            name="Data Visualization Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        description = context.get("task_description", "Visualização de dados analítica")

        system_prompt = (
            "Você é um especialista em visualização de dados. Gere código Python limpo (matplotlib/seaborn) "
            "que carregue os dados, produza gráficos adequados (barras, linhas, histogramas, scatter) "
            "com títulos, legendas, eixos rotulados e salve a figura em arquivo. "
            "Responda SOMENTE com o código Python, sem markdown formatting (```python)."
        )
        user_prompt = f"Descrição: {description}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        code = resp.content or ""
        code = re.sub(r'^```[\w]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'```$', '', code, flags=re.MULTILINE).strip()

        result = {"visualize.py": code}
        self.validate_output(result)
        return result

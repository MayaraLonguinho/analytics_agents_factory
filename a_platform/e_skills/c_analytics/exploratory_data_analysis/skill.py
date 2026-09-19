import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class ExploratoryDataAnalysisSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="exploratory-data-analysis",
            name="Exploratory Data Analysis Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        description = context.get("task_description", "Análise exploratória de dados")
        dataset_path = context.get("dataset_path", "")

        system_prompt = (
            "Você é um cientista de dados especialista em análise exploratória de dados (EDA). "
            "Gere um script Python completo usando Pandas que carregue os dados, compute métricas de dispersão, "
            "frequências categóricas, correlações e resumos descritivos. "
            "Responda SOMENTE com o código Python, sem markdown formatting (```python)."
        )
        user_prompt = f"Dataset: {dataset_path}\nDescrição: {description}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        code = resp.content or ""
        code = re.sub(r'^```[\w]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'```$', '', code, flags=re.MULTILINE).strip()

        result = {"eda.py": code}
        self.validate_output(result)
        return result

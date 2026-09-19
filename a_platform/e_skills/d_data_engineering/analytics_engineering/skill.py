import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class AnalyticsEngineeringSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="analytics-engineering",
            name="Analytics Engineering Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        tech = context.get("database_technology", "SQLite")
        description = context.get("task_description", "Modelagem modular de analytics")

        system_prompt = (
            f"Você é um Analytics Engineer sênior. Gere modelos SQL modulares para {tech}, "
            "estruturados em camadas (staging, intermediate e marts), com CTEs limpas e documentadas. "
            "Responda SOMENTE com o código SQL, sem markdown formatting (```sql)."
        )
        user_prompt = f"Banco: {tech}\nDescrição: {description}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        code = resp.content or ""
        code = re.sub(r'^```[\w]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'```$', '', code, flags=re.MULTILINE).strip()

        result = {"analytics_models.sql": code}
        self.validate_output(result)
        return result

import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class DimensionalModelingSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="dimensional-modeling",
            name="Dimensional Modeling Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        tech = context.get("database_technology", "SQLite")
        description = context.get("task_description", "Modelagem dimensional de dados")

        system_prompt = (
            f"Você é um Arquiteto de Dados especialista em Modelagem Dimensional (Kimball). "
            f"Gere o script SQL DDL para {tech} com criação de tabelas fato (fact_*) e dimensão (dim_*), "
            "chaves primárias e relacionamentos com integridade referencial. "
            "Responda SOMENTE com o código SQL, sem markdown formatting (```sql)."
        )
        user_prompt = f"Banco: {tech}\nDescrição: {description}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        code = resp.content or ""
        code = re.sub(r'^```[\w]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'```$', '', code, flags=re.MULTILINE).strip()

        result = {"dimensional_model.sql": code}
        self.validate_output(result)
        return result

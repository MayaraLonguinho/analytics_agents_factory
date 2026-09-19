import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class SqlOptimizationSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="sql-optimization",
            name="SQL Optimization Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        tech = context.get("database_technology", "SQLite")
        description = context.get("task_description", "Otimização de queries SQL")

        system_prompt = (
            f"Você é um Database Administrator e Arquiteto de Dados especialista em {tech}. "
            "Analise a query fornecida e gere a versão otimizada com índices apropriados e DDL necessária. "
            "Responda SOMENTE com o código SQL, sem markdown formatting (```sql)."
        )
        user_prompt = f"Banco: {tech}\nDescrição: {description}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        code = resp.content or ""
        code = re.sub(r'^```[\w]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'```$', '', code, flags=re.MULTILINE).strip()

        result = {"optimized_queries.sql": code}
        self.validate_output(result)
        return result

import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill, ParameterDefinition
# pyrefly: ignore [missing-import]
from a_platform.j_llm_gateway import LLMGateway

logger = logging.getLogger(__name__)

class SqlGenerationSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="sql_generation",
            name="SQL Generation Skill",
            input_schema=[
                ParameterDefinition(name="database_technology", data_type="string", required=True),
                ParameterDefinition(name="schema_definition", data_type="string", required=True),
            ],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)

        tech = context["database_technology"]
        schema = context["schema_definition"]
        description = context.get("task_description", "")
        project_plan = context.get("project_plan", {})

        logger.info(f"[SqlGenerationSkill] Gerando SQL para {tech} usando LLM")

        system_prompt = (
            "Você é um engenheiro de dados especialista em SQL. "
            "Sua tarefa é gerar scripts SQL limpos (DDL/DML) baseados nos requisitos e schema. "
            "Responda SOMENTE com o código SQL. Não use markdown formatting (```sql) na resposta."
        )
        user_prompt = (
            f"Banco: {tech}\nDescrição: {description}\n"
            f"Schema: {schema}\nPlan: {project_plan}\n\nGere o script completo (schema.sql)."
        )

        llm_response = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)

        if not llm_response.content:
            msg = "[SqlGenerationSkill] LLM retornou conteúdo vazio."
            logger.error(msg)
            raise ValueError(msg)

        code_text = llm_response.content
        code_text = re.sub(r'^```[\w]*\n', '', code_text, flags=re.MULTILINE)
        code_text = re.sub(r'```$', '', code_text, flags=re.MULTILINE).strip()

        result = {"schema.sql": code_text}
        self.validate_output(result)
        return result

import logging
import re
from typing import Dict, Any
from a_platform.e_skills.skill_contract import BaseSkill, CORE_SKILL_CONTRACTS
from a_platform.g_llm_gateway.gateway import LLMGateway

logger = logging.getLogger(__name__)

class SqlGenerationSkill(BaseSkill):
    def __init__(self):
        super().__init__(contract=CORE_SKILL_CONTRACTS["sql_generation"])
        self.llm = LLMGateway()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        
        tech = context["database_technology"]
        schema = context["schema_definition"]
        description = context.get("task_description", "")
        project_plan = context.get("project_plan", {})
        
        logger.info(f"[SqlGenerationSkill] Gerando SQL para {tech} usando LLM")
        
        system_prompt = (
            "Você é um engenheiro de dados especialista em SQL. "
            "Sua tarefa é gerar scripts SQL limpos (DDL/DML) ou consultas baseadas nos requisitos e schema. "
            "Responda SOMENTE com o código SQL. Não inclua texto ao redor. Não use markdown formatting (```sql) na resposta, APENAS O CÓDIGO."
        )

        user_prompt = f"Banco: {tech}\nDescrição: {description}\nSchema: {schema}\nPlan: {project_plan}\n\nGere o script completo (schema.sql)."

        llm_response = self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        if llm_response["success"]:
            code_text = llm_response["text"]
            code_text = re.sub(r'^```[\w]*\n', '', code_text, flags=re.MULTILINE)
            code_text = re.sub(r'```$', '', code_text, flags=re.MULTILINE).strip()
        else:
            logger.error(f"[SqlGenerationSkill] Falha LLM: {llm_response.get('error')}")
            code_text = f"-- LLM Generation Failed: {llm_response.get('error')}\nCREATE TABLE generated_table (id INT PRIMARY KEY);"
        
        result = {
            "schema.sql": code_text
        }
        
        self.validate_output(result)
        return result

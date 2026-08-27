import logging
import re
from typing import Dict, Any
from a_platform.e_skills.skill_contract import BaseSkill, CORE_SKILL_CONTRACTS
from a_platform.g_llm_gateway.gateway import LLMGateway

logger = logging.getLogger(__name__)

class EtlScriptingSkill(BaseSkill):
    def __init__(self):
        super().__init__(contract=CORE_SKILL_CONTRACTS["etl_scripting"])
        self.llm = LLMGateway()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        
        tool = context["data_processing_tool"]
        description = context.get("task_description", "")
        dataset_profile = context.get("dataset_profile", {})
        project_plan = context.get("project_plan", {})
        
        logger.info(f"[EtlScriptingSkill] Gerando script ETL para {tool} usando LLM")
        
        system_prompt = (
            "Você é um engenheiro de dados sênior especializado em ETL. "
            "Gere o script de ETL Python limpo, documentado, tipado e com tratamento de erros. "
            "Responda SOMENTE com o código do script solicitado. Não inclua texto ao redor nem markdown formatting (```python) na resposta."
        )

        user_prompt = f"Ferramenta: {tool}\nDescrição: {description}\nDataset Profile: {dataset_profile}\nPlan: {project_plan}"

        llm_response = self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        if llm_response["success"]:
            code_text = llm_response["text"]
            code_text = re.sub(r'^```[\w]*\n', '', code_text, flags=re.MULTILINE)
            code_text = re.sub(r'```$', '', code_text, flags=re.MULTILINE).strip()
        else:
            logger.error(f"[EtlScriptingSkill] Falha LLM: {llm_response.get('error')}")
            code_text = f"# LLM Generation Failed: {llm_response.get('error')}\nprint('Fallback ETL')"
        
        result = {
            "etl.py": code_text
        }
        
        self.validate_output(result)
        return result

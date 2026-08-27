import logging
import re
from typing import Dict, Any
from a_platform.e_skills.skill_contract import BaseSkill, CORE_SKILL_CONTRACTS
from a_platform.g_llm_gateway.gateway import LLMGateway

logger = logging.getLogger(__name__)

class BasicCodingSkill(BaseSkill):
    def __init__(self):
        super().__init__(contract=CORE_SKILL_CONTRACTS["basic_coding"])
        self.llm = LLMGateway()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        
        script_name = context["script_name"]
        description = context.get("task_description", "")
        project_plan = context.get("project_plan", {})
        discovery = context.get("discovery_requirements", {})
        architecture = context.get("architecture_context", {})
        rules = context.get("brain_rules", [])

        logger.info(f"[BasicCodingSkill] Gerando código para {script_name} usando LLM")
        
        system_prompt = (
            "Você é um engenheiro de software sênior. Sua tarefa é gerar código limpo, documentado, tipado e funcional. "
            "Responda SOMENTE com o código do arquivo solicitado. Não inclua texto ao redor. Não use markdown formatting (```python) na resposta, APENAS O CÓDIGO."
        )

        user_prompt = f"Gere o arquivo {script_name} considerando:\nDescrição: {description}\nRegras: {rules}\nArquitetura: {architecture}\nDiscovery: {discovery}\nPlan: {project_plan}"

        llm_response = self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        if not llm_response.get("success"):
            error_msg = f"LLM Generation Failed: {llm_response.get('error')}"
            logger.error(f"[BasicCodingSkill] {error_msg}")
            raise ValueError(error_msg)
            
        code_text = llm_response["text"]
        # Clean up markdown if model ignored the instruction
        code_text = re.sub(r'^```[\w]*\n', '', code_text, flags=re.MULTILINE)
        code_text = re.sub(r'```$', '', code_text, flags=re.MULTILINE).strip()
        
        result = {
            script_name: code_text
        }
        
        self.validate_output(result)
        return result

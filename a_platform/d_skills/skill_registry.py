import logging
from typing import Dict, Any

from a_platform.d_skills.skill_contract import CORE_SKILL_CONTRACTS, BaseSkill
from a_platform.f_llm_gateway.gateway import LLMGateway

logger = logging.getLogger(__name__)

class GenericLLMSkill(BaseSkill):
    def __init__(self, contract, system_prompt: str):
        super().__init__(contract)
        self.system_prompt = system_prompt
        self.gateway = LLMGateway()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Context: {context}\nGerar os seguintes artefatos: {self.contract.expected_outputs}"
        res = self.gateway.generate_text(prompt, system_prompt=self.system_prompt)
        content = res.get("text", "")
        # Fallback de mock se falhar
        if not res.get("success"):
            content = "Gerado via fallback: " + str(self.contract.expected_outputs)
            
        result = {}
        for out in self.contract.expected_outputs:
            # Mock extracting content for each expected output
            result[out] = content
            
        return result

class SkillRegistry:
    """
    Centraliza a execução das Skills que os agentes podem solicitar, agora validando contratos.
    """
    def __init__(self):
        self.contracts = CORE_SKILL_CONTRACTS
        
        # Registra instâncias reais de skills
        self.skills = {
            "sql_generation": GenericLLMSkill(
                self.contracts["sql_generation"], 
                "Você é um DBA. Escreva schemas SQL válidos."
            ),
            "api_design": GenericLLMSkill(
                self.contracts["api_design"], 
                "Você é um Arquiteto de API. Escreva o Swagger/OpenAPI."
            ),
            "dataset_profiling": GenericLLMSkill(
                self.contracts["dataset_profiling"], 
                "Você é um Data Scientist. Escreva um JSON com profile dos dados."
            ),
            "etl_scripting": GenericLLMSkill(
                self.contracts["etl_scripting"], 
                "Você é um Data Engineer. Escreva o script Python ETL."
            ),
            "basic_coding": GenericLLMSkill(
                self.contracts["basic_coding"], 
                "Você é um Dev Python. Escreva o script de acordo com a solicitação."
            )
        }

    def run_skill(self, skill_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"[SkillRegistry] Invocando skill: {skill_name}")
        
        try:
            if skill_name not in self.skills:
                return {"success": False, "error": f"Skill '{skill_name}' desconhecida."}
                
            skill_impl = self.skills[skill_name]
            
            # Valida input
            skill_impl.validate_input(context)
            
            # Executa
            result = skill_impl.execute(context)
            
            # Valida output
            skill_impl.validate_output(result)
            
            # Formata saída no padrão legado provisoriamente (apenas 1 artefato esperado ou lista)
            first_artifact = list(result.keys())[0] if result else "unknown"
            content = result.get(first_artifact, "")
            
            return {"success": True, "artifact": first_artifact, "content": content}
            
        except ValueError as ve:
            logger.error(f"[SkillRegistry] Erro de contrato: {ve}")
            return {"success": False, "error": str(ve)}
        except Exception as e:
            logger.error(f"[SkillRegistry] Falha na skill {skill_name}: {e}")
            return {"success": False, "error": str(e)}

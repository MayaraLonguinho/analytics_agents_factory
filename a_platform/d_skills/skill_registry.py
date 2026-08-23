import logging
from typing import Dict, Any

from a_platform.d_skills.skill_contract import CORE_SKILL_CONTRACTS

logger = logging.getLogger(__name__)

class SkillRegistry:
    """
    Centraliza a execução das Skills que os agentes podem solicitar, agora validando contratos.
    """
    def __init__(self):
        self.contracts = CORE_SKILL_CONTRACTS

    def run_skill(self, skill_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"[SkillRegistry] Invocando skill: {skill_name}")
        
        try:
            if skill_name not in self.contracts:
                return {"success": False, "error": f"Skill '{skill_name}' desconhecida."}
                
            contract = self.contracts[skill_name]
            contract.validate_inputs(context)
            
            # Executa a implementação baseada no nome
            if skill_name == "sql_generation":
                return self._skill_sql_generation(context)
            elif skill_name == "api_design":
                return self._skill_api_design(context)
            elif skill_name == "dataset_profiling":
                return {"success": True, "artifact": "dataset_profile.json", "content": "{}"}
            elif skill_name == "etl_scripting":
                return self._skill_etl_scripting(context)
            elif skill_name == "basic_coding":
                script_name = context.get("script_name", "script.py")
                return {"success": True, "artifact": script_name, "content": "print('Hello World')"}
            else:
                return {"success": False, "error": f"Skill '{skill_name}' não possui implementação conectada."}
        except ValueError as ve:
            logger.error(f"[SkillRegistry] Erro de contrato: {ve}")
            return {"success": False, "error": str(ve)}
        except Exception as e:
            logger.error(f"[SkillRegistry] Falha na skill {skill_name}: {e}")
            return {"success": False, "error": str(e)}

    def _skill_sql_generation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        db_type = context.get("database_technology", "PostgreSQL")
        schema_def = context.get("schema_definition", "CREATE TABLE main (id INT);")
        sql = f"-- Gerado para {db_type}\n{schema_def}"
        return {"success": True, "artifact": "schema.sql", "content": sql}

    def _skill_api_design(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"success": True, "artifact": "swagger.yaml", "content": "openapi: 3.0.0\ninfo:\n  title: API"}

    def _skill_etl_scripting(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"success": True, "artifact": "etl.py", "content": "def run_etl(): pass"}

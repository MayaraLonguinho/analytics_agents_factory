import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SkillRegistry:
    """
    Centraliza a execução das Skills que os agentes podem solicitar.
    """
    def __init__(self):
        pass

    def run_skill(self, skill_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"[SkillRegistry] Invocando skill: {skill_name}")
        
        try:
            if skill_name == "sql_generation":
                return self._skill_sql_generation(context)
            elif skill_name == "api_design":
                return self._skill_api_design(context)
            elif skill_name == "dataset_profiling":
                # Já executada globalmente antes, mas pode reexecutar
                return {"success": True, "artifact": "dataset_profile.json", "content": "{}"}
            elif skill_name == "etl_scripting":
                return self._skill_etl_scripting(context)
            elif skill_name == "basic_coding":
                return {"success": True, "artifact": "app.py", "content": "print('Hello World')"}
            else:
                return {"success": False, "error": f"Skill '{skill_name}' desconhecida."}
        except Exception as e:
            logger.error(f"[SkillRegistry] Falha na skill {skill_name}: {e}")
            return {"success": False, "error": str(e)}

    def _skill_sql_generation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        db_type = context.get("database_technology", "PostgreSQL")
        sql = f"-- Gerado para {db_type}\nCREATE TABLE main (id INT, data VARCHAR);"
        return {"success": True, "artifact": "schema.sql", "content": sql}

    def _skill_api_design(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"success": True, "artifact": "swagger.yaml", "content": "openapi: 3.0.0\ninfo:\n  title: API"}

    def _skill_etl_scripting(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"success": True, "artifact": "etl.py", "content": "def run_etl(): pass"}

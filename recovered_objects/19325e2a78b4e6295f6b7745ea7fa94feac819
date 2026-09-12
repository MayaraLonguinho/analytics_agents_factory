import logging
from typing import Dict, Any

from a_platform.e_skills.i_skill_contract import CORE_SKILL_CONTRACTS
from a_platform.e_skills.b_dataset.a_profiling.a_dataset_profiler import DatasetProfilingSkill
from a_platform.e_skills.c_analytics.a_sql_generation import SqlGenerationSkill
from a_platform.e_skills.d_data_engineering.a_etl_scripting import EtlScriptingSkill
from a_platform.e_skills.e_development.b_basic_coding import BasicCodingSkill
from a_platform.e_skills.e_development.a_api_design import ApiDesignSkill
from a_platform.e_skills.e_development.f_consolidation_skills import (
    CleaningSkill, DeduplicationSkill, CategorizationSkill, AnalyticsSkill,
    DashboardSkill, ChatbotSkill, BackendSkill, FrontendSkill, TestingSkill,
    DocumentationSkill, DockerSkill
)

logger = logging.getLogger(__name__)

class SkillRegistry:
    """
    Centraliza a execução das Skills que os agentes podem solicitar, agora validando contratos.
    """
    def __init__(self):
        self.contracts = CORE_SKILL_CONTRACTS
        
        # Registra instâncias reais de skills
        self.skills = {
            "sql_generation": SqlGenerationSkill(),
            "api_design": ApiDesignSkill(),
            "dataset_profiling": DatasetProfilingSkill(),
            "etl_scripting": EtlScriptingSkill(),
            "basic_coding": BasicCodingSkill(),
            "cleaning": CleaningSkill(),
            "deduplication": DeduplicationSkill(),
            "categorization": CategorizationSkill(),
            "analytics": AnalyticsSkill(),
            "dashboard": DashboardSkill(),
            "chatbot": ChatbotSkill(),
            "backend": BackendSkill(),
            "frontend": FrontendSkill(),
            "testing": TestingSkill(),
            "documentation": DocumentationSkill(),
            "docker": DockerSkill()
        }

    def get_skill(self, name: str):
        return self.skills.get(name)

    def run_skill(self, skill_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"[SkillRegistry] Invocando skill: {skill_name}")
        
        try:
            if skill_name not in self.skills:
                return {"success": False, "error": f"Skill '{skill_name}' desconhecida."}
                
            skill_impl = self.skills[skill_name]
            
            # Valida input
            skill_impl.validate_input(context)
            
            import asyncio
            import inspect
            if inspect.iscoroutinefunction(skill_impl.execute):
                result = asyncio.run(skill_impl.execute(context))
            else:
                result = skill_impl.execute(context)
            
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

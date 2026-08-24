import logging
from typing import Dict, Any
from a_platform.e_skills.skill_contract import BaseSkill, CORE_SKILL_CONTRACTS

logger = logging.getLogger(__name__)

class BasicCodingSkill(BaseSkill):
    def __init__(self):
        super().__init__(contract=CORE_SKILL_CONTRACTS["basic_coding"])

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        
        script_name = context["script_name"]
        logger.info(f"[BasicCodingSkill] Gerando código base para {script_name}")
        
        result = {
            "script.py": f"print('Hello from {script_name}')"
        }
        
        self.validate_output(result)
        return result

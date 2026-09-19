import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.e_skills.b_etl.a_etl_scripting import EtlScriptingSkill

logger = logging.getLogger(__name__)

class EtlPipelineSkill(EtlScriptingSkill):
    """
    Evolução canônica da EtlScriptingSkill para etl-pipeline.
    Garante compatibilidade total com etl_scripting.
    """
    def __init__(self, **data: Any):
        super().__init__(**data)
        self.skill_id = "etl-pipeline"
        self.name = "ETL Pipeline Skill"

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        res = await super().execute(context)
        # Assegurar que 'pipeline.py' seja disponibilizado se 'etl.py' foi gerado
        if "etl.py" in res and "pipeline.py" not in res:
            res["pipeline.py"] = res["etl.py"]
        self.validate_output(res)
        return res

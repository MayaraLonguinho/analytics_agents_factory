import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.e_skills.d_analytics.a_sql_generation import SqlGenerationSkill

logger = logging.getLogger(__name__)

class SqlAnalyticsSkill(SqlGenerationSkill):
    """
    Evolução canônica de SqlGenerationSkill para sql-analytics.
    Compatível com sql_generation.
    """
    def __init__(self, **data: Any):
        super().__init__(**data)
        self.skill_id = "sql-analytics"
        self.name = "SQL Analytics Skill"

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Suportar defaults para evitar falhas se database_technology não vier informado
        if "database_technology" not in context:
            context["database_technology"] = context.get("architecture", {}).get("database_technology", "SQLite")
        if "schema_definition" not in context:
            context["schema_definition"] = "CREATE TABLE IF NOT EXISTS main_table (id INT);"
            
        res = await super().execute(context)
        if "schema.sql" in res and "analytics.sql" not in res:
            res["analytics.sql"] = res["schema.sql"]
        self.validate_output(res)
        return res

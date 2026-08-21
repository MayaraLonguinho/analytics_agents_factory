from typing import Optional
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.f_llm_gateway.gateway import LLMGateway

class ETLAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    async def execute(self, task_name: str) -> Artifact:
        return Artifact(name="etl_script", path="etl.py", content="# ETL pipeline")

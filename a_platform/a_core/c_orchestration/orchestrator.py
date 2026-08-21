from typing import Any, Dict
from pydantic import BaseModel, Field

class OrchestratorConfig(BaseModel):
    max_retries: int = 3
    timeout_seconds: int = 300

class BaseOrchestrator:
    def __init__(self, config: OrchestratorConfig = OrchestratorConfig()):
        self.config = config

    def orchestrate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

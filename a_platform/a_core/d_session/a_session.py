import uuid
from typing import Dict, Any, Optional

from a_platform.a_core.d_session.b_context import ExecutionContext
from a_platform.a_core.d_session.c_state import StateManager

class AAFSession:
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.context = ExecutionContext()
        self.state_manager = StateManager(project_id=self.session_id)
        self.status = "INITIALIZED"
        self.metadata: Dict[str, Any] = {}

    def get_context(self) -> ExecutionContext:
        return self.context

    def update_state(self, key: str, value: Any) -> None:
        self.state_manager.set_state(key, value)

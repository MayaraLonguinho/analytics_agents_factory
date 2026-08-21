from typing import Any, Dict, List
from datetime import datetime, timezone

class StateManager:
    def __init__(self):
        self.state: Dict[str, Any] = {}
        self.history: List[Dict[str, Any]] = []

    def update_state(self, key: str, value: Any, actor: str = "system") -> None:
        old_value = self.state.get(key)
        self.state[key] = value
        self._record_transition(key, old_value, value, actor)

    def _record_transition(self, key: str, old_value: Any, new_value: Any, actor: str) -> None:
        transition = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "key": key,
            "old_value": old_value,
            "new_value": new_value,
            "actor": actor
        }
        self.history.append(transition)

    def get_state(self, key: str) -> Any:
        return self.state.get(key)

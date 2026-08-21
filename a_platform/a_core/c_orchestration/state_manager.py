from typing import Dict, Any

class StateManager:
    def __init__(self):
        self.state: Dict[str, Any] = {
            "prompt": None,
            "project_plan": None,
            "artifacts": [],
            "project_dir": None,
            "certification": None,
            "status": "INITIALIZED"
        }

    def update(self, key: str, value: Any):
        self.state[key] = value

    def get(self, key: str) -> Any:
        return self.state.get(key)

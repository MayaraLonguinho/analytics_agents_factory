from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

class MemoryManager:
    def __init__(self):
        self.session_history: Dict[str, List[Dict[str, Any]]] = {}
        self.architectural_decisions: Dict[str, List[Dict[str, Any]]] = {}
        self.execution_memory: Dict[str, Dict[str, Any]] = {}

    def store_session_history(self, session_id: str, entry: Dict[str, Any]) -> None:
        if session_id not in self.session_history:
            self.session_history[session_id] = []
        entry["timestamp"] = datetime.now(timezone.utc).isoformat()
        self.session_history[session_id].append(entry)

    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        return self.session_history.get(session_id, [])

    def store_architectural_decision(self, project_id: str, decision: Dict[str, Any]) -> None:
        if project_id not in self.architectural_decisions:
            self.architectural_decisions[project_id] = []
        decision["timestamp"] = datetime.now(timezone.utc).isoformat()
        self.architectural_decisions[project_id].append(decision)

    def get_architectural_decisions(self, project_id: str) -> List[Dict[str, Any]]:
        return self.architectural_decisions.get(project_id, [])

    def store_execution_memory(self, execution_id: str, data: Dict[str, Any]) -> None:
        self.execution_memory[execution_id] = data
        self.execution_memory[execution_id]["updated_at"] = datetime.now(timezone.utc).isoformat()

    def get_execution_memory(self, execution_id: str) -> Optional[Dict[str, Any]]:
        return self.execution_memory.get(execution_id)

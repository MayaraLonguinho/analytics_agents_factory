from typing import Dict, Any

class LLMRouter:
    def __init__(self):
        self.routes = {}
        
    def route(self, task_complexity: str) -> str:
        if task_complexity == "high":
            return "openai"
        return "ollama"

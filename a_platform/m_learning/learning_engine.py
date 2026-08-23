import logging
import os
import json
from typing import Dict, Any

from a_platform.a_core.b_domain.project_request import ProjectRequest

logger = logging.getLogger(__name__)

class LearningEngine:
    """
    Guarda logs de erros e correções na Memória (Brain)
    para não repetir os mesmos erros.
    """
    def __init__(self):
        self.memory_path = os.path.join(os.path.dirname(__file__), "..", "b_brain", "memory.json")
        self.memory = self._load_memory()

    def _load_memory(self) -> list:
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_memory(self):
        try:
            os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
            with open(self.memory_path, "w") as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            logger.error(f"[LearningEngine] Falha ao salvar memória: {e}")

    def log_correction(self, request: ProjectRequest, error_log: str, correction: str):
        logger.info("[LearningEngine] Registrando correção no Brain...")
        entry = {
            "project_id": request.project_id,
            "error": error_log,
            "correction_applied": correction
        }
        self.memory.append(entry)
        self._save_memory()
        logger.info("[LearningEngine] Correção memorizada com sucesso.")

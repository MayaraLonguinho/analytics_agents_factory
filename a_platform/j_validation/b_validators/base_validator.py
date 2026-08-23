from abc import ABC, abstractmethod
from typing import Dict, Any
from a_platform.a_core.b_domain.project_request import ProjectRequest
import logging

logger = logging.getLogger(__name__)

class BaseValidator(ABC):
    """
    Base class para todos os validadores especializados da fábrica.
    Cada validador é responsável por uma checagem restrita do projeto gerado.
    """
    @abstractmethod
    def validate(self, request: ProjectRequest, project_dir: str) -> Dict[str, Any]:
        """
        Retorna um dicionário:
        {
            "success": bool,
            "status": "PASS" | "FAIL" | "NOT_APPLICABLE",
            "message": str
        }
        """
        pass

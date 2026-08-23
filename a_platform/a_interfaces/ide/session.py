import logging
from typing import Optional, Tuple
from a_platform.a_core.c_orchestration.state_manager import StateManager
from a_platform.a_core.b_domain.project_request import ProjectRequest

logger = logging.getLogger(__name__)

class IDESession:
    """
    Controla o ciclo de vida e recuperação da sessão do projeto para a IDE.
    """
    @staticmethod
    def load_session(project_id: str) -> Tuple[Optional[StateManager], Optional[ProjectRequest]]:
        try:
            state_manager, request = StateManager.load_state(project_id)
            return state_manager, request
        except FileNotFoundError:
            logger.error(f"[IDESession] Sessão não encontrada para {project_id}")
            return None, None
            
    @staticmethod
    def delete_session(project_id: str) -> bool:
        import os
        state_file = os.path.join(os.getcwd(), ".aaf_state", f"{project_id}.json")
        if os.path.exists(state_file):
            os.remove(state_file)
            return True
        return False

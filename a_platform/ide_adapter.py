import logging
import uuid
from typing import Dict, Any, Optional

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.c_orchestration.orchestrator import MasterOrchestrator
from a_platform.a_core.c_orchestration.state_manager import StateManager

logger = logging.getLogger(__name__)

class IDEAdapter:
    """
    Adapter para integrar a Analytics Agents Factory com a IDE e interfaces MCP.
    Gerencia criação, retomada após interrupções (ex: Discovery) e status.
    """
    def __init__(self):
        pass

    def create_project(self, prompt: str, dataset_path: Optional[str] = None, domain: Optional[str] = None) -> Dict[str, Any]:
        project_id = f"proj_{uuid.uuid4().hex[:8]}"
        request = ProjectRequest(
            prompt=prompt,
            dataset_path=dataset_path,
            domain=domain,
            project_id=project_id
        )
        
        # Inicia histórico de conversas
        request.discovery_data["history"] = []
        
        orchestrator = MasterOrchestrator()
        return self._execute_and_format(orchestrator, request)

    def continue_project(self, project_id: str, user_response: str) -> Dict[str, Any]:
        try:
            state_manager, request = StateManager.load_state(project_id)
        except FileNotFoundError:
            return {"success": False, "error": f"Projeto {project_id} não encontrado ou expirou.", "status": "FAILED"}
            
        # Adiciona resposta no histórico do Discovery
        history = request.discovery_data.get("history", [])
        
        # Recuperamos a pergunta pendente para parear com a resposta
        last_q = request.discovery_data.get("missing_info_question", "Question missing")
        history.append({"role": "assistant", "content": last_q})
        history.append({"role": "user", "content": user_response})
        
        request.discovery_data["history"] = history
        
        # Limpamos a pergunta pendente
        if "missing_info_question" in request.discovery_data:
            del request.discovery_data["missing_info_question"]
            
        orchestrator = MasterOrchestrator()
        return self._execute_and_format(orchestrator, request, state_manager)

    def get_project_status(self, project_id: str) -> Dict[str, Any]:
        try:
            state_manager, _ = StateManager.load_state(project_id)
            return {"success": True, "status": state_manager.get_status()}
        except FileNotFoundError:
            return {"success": False, "error": f"Projeto {project_id} não encontrado.", "status": "NOT_FOUND"}

    def _execute_and_format(self, orchestrator: MasterOrchestrator, request: ProjectRequest, existing_state: Optional[StateManager] = None) -> Dict[str, Any]:
        result = orchestrator.execute_pipeline(request, existing_state=existing_state)
        
        if result == "PAUSED":
            # Retorna a pergunta do Discovery para a IDE
            question = request.discovery_data.get("missing_info_question", "Por favor, forneça mais detalhes sobre sua solicitação.")
            return {
                "success": True,
                "project_id": request.project_id,
                "status": "NEEDS_INPUT",
                "message": question
            }
        elif result == "SUCCESS":
            return {
                "success": True,
                "project_id": request.project_id,
                "status": "READY",
                "message": "Projeto gerado e certificado com sucesso."
            }
        else:
            return {
                "success": False,
                "project_id": request.project_id,
                "status": "FAILED",
                "error": orchestrator.state_manager.get_status() if orchestrator.state_manager else "Unknown error"
            }

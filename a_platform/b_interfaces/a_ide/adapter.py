import logging
import uuid
from typing import Optional
from dataclasses import asdict

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.c_orchestration.orchestrator import MasterOrchestrator
from a_platform.b_interfaces.a_ide.protocol import ProjectResponseDTO
from a_platform.b_interfaces.a_ide.session import IDESession

logger = logging.getLogger(__name__)

class IDEAdapter:
    """
    Adapter canônico para integrar a Analytics Agents Factory com a IDE e interfaces MCP.
    Substitui adapters isolados. É a única porta de entrada para a plataforma.
    """
    def __init__(self):
        pass

    def create_project(self, prompt: str, dataset_path: Optional[str] = None, domain: Optional[str] = None) -> ProjectResponseDTO:
        project_id = f"proj_{uuid.uuid4().hex[:8]}"
        request = ProjectRequest(
            prompt=prompt,
            dataset_path=dataset_path,
            domain=domain,
            project_id=project_id
        )
        
        request.discovery_data["history"] = []
        
        orchestrator = MasterOrchestrator()
        return self._execute_and_format(orchestrator, request)

    def start_project(self, prompt: str, dataset_path: Optional[str] = None, domain: Optional[str] = None) -> ProjectResponseDTO:
        return self.create_project(prompt, dataset_path, domain)

    def run_project(self, prompt: str, dataset_path: Optional[str] = None, domain: Optional[str] = None) -> ProjectResponseDTO:
        return self.create_project(prompt, dataset_path, domain)


    def continue_project(self, project_id: str, user_response: str) -> ProjectResponseDTO:
        state_manager, request = IDESession.load_session(project_id)
        if not state_manager or not request:
            return ProjectResponseDTO(
                success=False, 
                project_id=project_id, 
                status="FAILED", 
                error=f"Projeto {project_id} não encontrado."
            )
            
        history = request.discovery_data.get("history", [])
        last_q = request.discovery_data.get("missing_info_question", "Question missing")
        history.append({"role": "assistant", "content": last_q})
        history.append({"role": "user", "content": user_response})
        
        request.discovery_data["history"] = history
        if "missing_info_question" in request.discovery_data:
            del request.discovery_data["missing_info_question"]
            
        orchestrator = MasterOrchestrator()
        return self._execute_and_format(orchestrator, request, state_manager)

    def get_project_status(self, project_id: str) -> ProjectResponseDTO:
        state_manager, _ = IDESession.load_session(project_id)
        if not state_manager:
            return ProjectResponseDTO(
                success=False, 
                project_id=project_id, 
                status="NOT_FOUND", 
                error=f"Projeto {project_id} não encontrado."
            )
            
        return ProjectResponseDTO(
            success=True,
            project_id=project_id,
            status=state_manager.current_phase.name,
            details=state_manager.get_status()
        )

    def cancel_project(self, project_id: str) -> ProjectResponseDTO:
        if IDESession.delete_session(project_id):
            return ProjectResponseDTO(success=True, project_id=project_id, status="CANCELLED")
        return ProjectResponseDTO(success=False, project_id=project_id, status="NOT_FOUND")

    def get_project_result(self, project_id: str) -> ProjectResponseDTO:
        state_manager, request = IDESession.load_session(project_id)
        if not state_manager or not request:
            return ProjectResponseDTO(success=False, project_id=project_id, status="NOT_FOUND")
            
        if request.metadata.get("PROJECT_READY") == "YES":
            import os
            domain = request.discovery_data.get("domain", "generic").lower()
            path = os.path.join(os.getcwd(), "e_generated_projects", domain, project_id)
            return ProjectResponseDTO(
                success=True, 
                project_id=project_id, 
                status="READY", 
                details={"path": path}
            )
        return ProjectResponseDTO(success=False, project_id=project_id, status=state_manager.current_phase.name)

    def _execute_and_format(self, orchestrator: MasterOrchestrator, request: ProjectRequest, existing_state=None) -> ProjectResponseDTO:
        result = orchestrator.execute_pipeline(request, existing_state=existing_state)
        
        if result == "PAUSED":
            question = request.discovery_data.get("missing_info_question", "Forneça detalhes adicionais.")
            return ProjectResponseDTO(
                success=True,
                project_id=request.project_id,
                status="NEEDS_INPUT",
                message=question
            )
        elif result == "SUCCESS":
            return ProjectResponseDTO(
                success=True,
                project_id=request.project_id,
                status="READY",
                message="Projeto gerado e certificado com sucesso."
            )
        else:
            return ProjectResponseDTO(
                success=False,
                project_id=request.project_id,
                status="FAILED",
                error=str(orchestrator.state_manager.get_status() if orchestrator.state_manager else "Unknown error")
            )

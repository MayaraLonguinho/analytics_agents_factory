import logging
from typing import Dict, Any, Optional

from a_platform.a_core.c_orchestration.b_orchestrator import MasterOrchestrator
from a_platform.a_core.c_orchestration.c_state_manager import StateManager
from a_platform.a_core.b_domain.i_execution_context import ExecutionContext

logger = logging.getLogger(__name__)

class IDEAdapter:
    """
    Porta de entrada oficial da AAF para o IDE Agent e o CLI.
    """
    def __init__(self):
        self.orchestrator = MasterOrchestrator()

    def create_project(self, prompt: str, dataset_path: Optional[str] = None) -> Dict[str, Any]:
        """Inicia um novo projeto a partir de um prompt."""
        logger.info("[IDEAdapter] Iniciando novo projeto...")
        
        import uuid
        project_id = f"prj_{uuid.uuid4().hex[:8]}"
        
        req = ExecutionContext(
            prompt=prompt,
            project_id=project_id,
            dataset_path=dataset_path
        )
        
        try:
            status = self.orchestrator.execute_pipeline(req)
            
            sm = self.orchestrator.state_manager
            
            if status == "PAUSED" or sm.current_phase.name == "NEEDS_INPUT":
                last_q = ""
                if req.discovery_data and "history" in req.discovery_data:
                    history = req.discovery_data["history"]
                    if history:
                        last_entry = history[-1]
                        if last_entry.get("role") == "agent":
                            last_q = last_entry.get("content", "")
                
                return {
                    "project_id": project_id,
                    "status": "NEEDS_INPUT",
                    "question": last_q or "Por favor forneça mais contexto."
                }
            elif sm.project_ready:
                return {
                    "project_id": project_id,
                    "status": "SUCCESS",
                    "question": None
                }
            else:
                return {
                    "project_id": project_id,
                    "status": "FAILED",
                    "question": sm.phases[sm.current_phase].details.get("error", "Erro desconhecido")
                }
                
        except Exception as e:
            logger.error(f"[IDEAdapter] Erro ao criar projeto: {e}")
            return {
                "project_id": project_id,
                "status": "FAILED",
                "question": str(e)
            }

    def continue_project(self, project_id: str, answer: str) -> Dict[str, Any]:
        """Continua a execução de um projeto pausado com a resposta do usuário."""
        logger.info(f"[IDEAdapter] Continuando projeto {project_id}...")
        
        try:
            sm, req = StateManager.load_state(project_id)
            
            if sm.current_phase.name != "NEEDS_INPUT":
                return {
                    "project_id": project_id,
                    "status": "FAILED",
                    "question": f"O projeto não está aguardando input. Fase atual: {sm.current_phase.name}"
                }
                
            if "history" not in req.discovery_data:
                req.discovery_data["history"] = []
                
            req.discovery_data["history"].append({"role": "user", "content": answer})
            
            from a_platform.a_core.c_orchestration.c_state_manager import ProjectPhase, PhaseStatus
            sm.current_phase = ProjectPhase.DISCOVERY
            sm.phases[ProjectPhase.DISCOVERY].status = PhaseStatus.IN_PROGRESS
            sm.phases[ProjectPhase.NEEDS_INPUT].status = PhaseStatus.COMPLETED
            
            self.orchestrator.state_manager = sm
            
            status = self.orchestrator.execute_pipeline(req, existing_state=sm)
            
            if status == "PAUSED" or sm.current_phase.name == "NEEDS_INPUT":
                last_q = ""
                history = req.discovery_data.get("history", [])
                if history:
                    last_entry = history[-1]
                    if last_entry.get("role") == "agent":
                        last_q = last_entry.get("content", "")
                        
                return {
                    "project_id": project_id,
                    "status": "NEEDS_INPUT",
                    "question": last_q or "Por favor forneça mais contexto."
                }
            elif sm.project_ready:
                return {
                    "project_id": project_id,
                    "status": "SUCCESS",
                    "question": None
                }
            else:
                return {
                    "project_id": project_id,
                    "status": "FAILED",
                    "question": sm.phases[sm.current_phase].details.get("error", "Erro desconhecido")
                }
                
        except Exception as e:
            logger.error(f"[IDEAdapter] Erro ao continuar projeto: {e}")
            return {
                "project_id": project_id,
                "status": "FAILED",
                "question": str(e)
            }

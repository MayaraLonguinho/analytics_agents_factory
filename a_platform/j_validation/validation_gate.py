import logging
import os
from typing import Dict, Any

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.j_validation.c_gates.pre_execution import PreExecutionGate
from a_platform.j_validation.c_gates.post_execution import PostExecutionGate
from a_platform.j_validation.c_gates.project_ready import ProjectReadyGate

logger = logging.getLogger(__name__)

class ValidationGate:
    """
    Portão de Validação Principal.
    Garante estruturalmente que os componentes gerados estão corretos.
    Oquestra PreExecution, PostExecution e ProjectReady.
    """
    def __init__(self):
        self.pre = PreExecutionGate()
        self.post = PostExecutionGate()
        self.ready = ProjectReadyGate()

    def run_validation(self, request: ProjectRequest) -> bool:
        domain = request.discovery_data.get("domain", "generic").lower()
        project_dir = os.path.abspath(os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id))
        
        logger.info(f"[ValidationGate] Iniciando bateria completa de validações em {project_dir}")
        
        if not self.pre.evaluate(request, project_dir):
            logger.error("[ValidationGate] Falha no PreExecutionGate")
            return False
            
        if not self.post.evaluate(request, project_dir):
            logger.error("[ValidationGate] Falha no PostExecutionGate")
            return False
            
        if not self.ready.evaluate(request, project_dir):
            logger.error("[ValidationGate] Falha no ProjectReadyGate")
            return False
            
        logger.info("[ValidationGate] Validação final concluída com sucesso (ALL PASS).")
        return True

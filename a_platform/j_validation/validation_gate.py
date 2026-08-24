import logging
import os
import yaml
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
    Orquestra PreExecution, PostExecution e ProjectReady.
    """
    def __init__(self):
        self.pre = PreExecutionGate()
        self.post = PostExecutionGate()
        self.ready = ProjectReadyGate()
        
    def has_validator(self, name: str) -> bool:
        # Pega a lista de validadores do pre e do post, seus nomes base.
        names = [v.__class__.__name__.lower().replace("validator", "") for v in self.pre.validators] + \
                [v.__class__.__name__.lower().replace("validator", "") for v in self.post.validators]
        # Allow both validator_pytest and pytest
        clean_name = name.lower().replace("validator_", "")
        return clean_name in names or name.lower() in names

    def run_validation(self, request: ProjectRequest) -> bool:
        domain = request.discovery_data.get("domain", "generic").lower()
        project_dir = os.path.abspath(os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id))
        
        logger.info(f"[ValidationGate] Iniciando bateria completa de validações em {project_dir}")
        
        # Anti-permissivo: Se a execução falhou, Validation falha obrigatoriamente
        if "execution_error" in request.metadata or request.metadata.get("runtime_payload", {}).get("exit_code", 1) != 0:
            if getattr(request.project_plan, "execution_required", True):
                logger.error("[ValidationGate] Validation = FAIL porque a execução do Runtime falhou.")
                return False
                
        # Carrega domain.yaml para saber quais validadores são obrigatórios
        required_validators = []
        domain_file = os.path.join(os.getcwd(), "a_platform", "h_domains", domain, "domain.yaml")
        if os.path.exists(domain_file):
            try:
                with open(domain_file, "r") as f:
                    data = yaml.safe_load(f)
                    required_validators = [v.lower() for v in data.get("validators", [])]
            except Exception as e:
                logger.error(f"[ValidationGate] Falha ao ler domain.yaml: {e}")
        
        if not self.pre.evaluate(request, project_dir, required_validators):
            logger.error("[ValidationGate] Falha no PreExecutionGate")
            return False
            
        if not self.post.evaluate(request, project_dir, required_validators):
            logger.error("[ValidationGate] Falha no PostExecutionGate")
            return False
            
        if not self.ready.evaluate(request, project_dir):
            logger.error("[ValidationGate] Falha no ProjectReadyGate")
            return False
            
        logger.info("[ValidationGate] Validação final concluída com sucesso (ALL PASS).")
        return True

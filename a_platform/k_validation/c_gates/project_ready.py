import logging
from typing import Dict, Any, List
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.k_validation.b_validators.backend.backend import BackendValidator
from a_platform.k_validation.b_validators.frontend.frontend import FrontendValidator
from a_platform.k_validation.b_validators.database.database import DatabaseValidator
from a_platform.k_validation.b_validators.documentation.documentation import DocumentationValidator
from a_platform.k_validation.b_validators.infrastructure.infrastructure import InfrastructureValidator

logger = logging.getLogger(__name__)

class ProjectReadyGate:
    """
    Última porta. Valida se todas as peças do domínio específico (backend, db, infra) 
    estão consolidadas para certificar o projeto como "PROJECT READY".
    """
    def __init__(self):
        self.validators = [
            BackendValidator(),
            FrontendValidator(),
            DatabaseValidator(),
            DocumentationValidator(),
            InfrastructureValidator()
        ]
        
    def evaluate(self, request: ProjectRequest, project_dir: str) -> bool:
        logger.info("[ProjectReadyGate] Checagem final de adequação de componentes (Project Ready)...")
        all_passed = True
        
        # Obter os agentes do plano (camadas exigidas)
        required_agents = set()
        if request.project_plan and request.project_plan.tasks:
            required_agents = {task.agent for task in request.project_plan.tasks}
            
        # Mapeamento do nome do validador para o agente correspondente que criaria essa camada
        validator_to_agent = {
            "BackendValidator": "BackendAgent",
            "FrontendValidator": "FrontendAgent",
            "DatabaseValidator": "DatabaseAgent",
            "InfrastructureValidator": "InfrastructureAgent",
            "DocumentationValidator": "DocumentationAgent"
        }
        
        for val in self.validators:
            name = val.__class__.__name__
            agent_needed = validator_to_agent.get(name)
            
            # Se o plano existe, e a camada é de uma responsabilidade que não está no plano, pule a validação e dê NOT_APPLICABLE.
            if request.project_plan and agent_needed and agent_needed not in required_agents:
                logger.info(f"[ProjectReadyGate] {name} NOT_APPLICABLE (Camada '{agent_needed}' não exigida no ProjectPlan)")
                continue
                
            res = val.validate(request, project_dir)
            
            if res["status"] == "FAIL":
                logger.error(f"[ProjectReadyGate] {name} FALHOU: {res['message']}")
                all_passed = False
            elif res["status"] == "PASS":
                logger.info(f"[ProjectReadyGate] {name} PASS")
            else:
                logger.info(f"[ProjectReadyGate] {name} NOT_APPLICABLE")
                
        if not all_passed:
            request.metadata["validation_error"] = "ProjectReadyGate failed"
            
        return all_passed

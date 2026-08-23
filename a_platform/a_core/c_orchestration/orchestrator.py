import logging
from typing import Any, Optional

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.c_orchestration.state_manager import StateManager, ProjectPhase, PhaseStatus
from a_platform.c_agents.b_discovery.discovery_agent import DiscoveryAgent
from a_platform.d_skills.b_dataset.profiling.dataset_profiler import DatasetProfiler
from a_platform.b_brain.brain import Brain
from a_platform.b_brain.g_graph.graph_builder import GraphBuilder
from a_platform.c_agents.c_architecture.architecture_agent import ArchitectureAgent
from a_platform.h_domains.domain_registry import DomainRegistry
from a_platform.c_agents.d_planner.planner_agent import PlannerAgent
from a_platform.c_agents.agent_factory import AgentFactory
from a_platform.g_factory.a_project_factory.project_factory import ProjectFactory
from a_platform.g_factory.d_artifact_materializer.materializer import ArtifactMaterializer
from a_platform.e_mcp.mcp_executor import MCPExecutor
from a_platform.i_runtime.runtime_engine import RuntimeEngine
from a_platform.j_validation.validation_gate import ValidationGate
from a_platform.k_quality.quality_engine import QualityEngine
from a_platform.l_certification.certification_engine import CertificationEngine
from a_platform.m_learning.learning_engine import LearningEngine
from a_platform.m_learning.repair.repair_loop import RepairLoop

logger = logging.getLogger(__name__)

class MasterOrchestrator:
    def __init__(self):
        self.state_manager = None
        self.mcp = MCPExecutor()
        self.discovery_agent = DiscoveryAgent()
        self.dataset_profiler = DatasetProfiler()
        self.brain = Brain()
        self.graph_builder = GraphBuilder()
        self.architecture_agent = ArchitectureAgent(self.brain, self.graph_builder)
        self.domain_registry = DomainRegistry()
        self.planner_agent = PlannerAgent(self.domain_registry)
        self.agent_factory = AgentFactory()
        self.project_factory = ProjectFactory(self.agent_factory)
        self.materializer = ArtifactMaterializer(self.mcp)
        self.runtime_engine = RuntimeEngine()
        self.validation_gate = ValidationGate()
        self.quality_engine = QualityEngine()
        self.certification_engine = CertificationEngine()
        self.learning_engine = LearningEngine()
        self.repair_loop = RepairLoop(self.agent_factory, self.learning_engine)
        
        self.compiled_artifacts = []
        
    def execute_pipeline(self, request: ProjectRequest, existing_state: Optional[StateManager] = None) -> str:
        if existing_state:
            self.state_manager = existing_state
            logger.info(f"Retomando pipeline para {request.project_id}")
        else:
            self.state_manager = StateManager(request.project_id)
            logger.info(f"Iniciando novo pipeline para {request.project_id}")
        
        try:
            # 1. Discovery
            if not self._run_phase(ProjectPhase.DISCOVERY, self._step_discovery, request):
                if self.state_manager.current_phase == ProjectPhase.NEEDS_INPUT:
                    self.state_manager.save_state(request)
                    return "PAUSED"
                raise Exception("Discovery falhou.")
            
            # 2. Dataset Profiling
            self._run_phase(ProjectPhase.DATASET_PROFILING, self._step_dataset_profiling, request)
            
            # 3. Brain
            self._run_phase(ProjectPhase.BRAIN, self._step_brain, request)
            
            # 4. Architecture
            self._run_phase(ProjectPhase.ARCHITECTURE, self._step_architecture, request)
            
            # 5. Planner
            self._run_phase(ProjectPhase.PLANNER, self._step_planner, request)
            
            # 6. Project Factory
            self._run_phase(ProjectPhase.PROJECT_FACTORY, self._step_project_factory, request)
            
            # 7. Materializer
            self._run_phase(ProjectPhase.MATERIALIZATION, self._step_materialization, request)
            
            # 8. Execution & Validation Loop
            validated = False
            while not validated and self.state_manager.repair_attempts <= self.state_manager.max_repair_attempts:
                # 8a. Execution Runtime
                exec_success = self._run_phase(ProjectPhase.EXECUTION, self._step_execution, request)
                
                # 8b. Validation Gate
                validation_passed = self._run_phase(ProjectPhase.VALIDATION, self._step_validation, request)
                
                if exec_success and validation_passed:
                    validated = True
                else:
                    self.state_manager.repair_attempts += 1
                    logger.warning(f"Execução/Validação falhou. Tentativa de reparo {self.state_manager.repair_attempts}")
                    if self.state_manager.repair_attempts <= self.state_manager.max_repair_attempts:
                        # Aciona o Repair Loop
                        repair_success = self._run_phase(ProjectPhase.REPAIR_LOOP, self._step_repair, request)
                        if not repair_success:
                            raise Exception("Falha crítica no Repair Loop.")
                            
                    # Remove COMPLETION da execution e validation para rodar dnv
                    self.state_manager.phases[ProjectPhase.EXECUTION].status = PhaseStatus.PENDING
                    self.state_manager.phases[ProjectPhase.VALIDATION].status = PhaseStatus.PENDING
            
            if not validated:
                raise Exception("Validação falhou após o limite máximo de tentativas de reparo.")
            
            # 9. Quality Engine
            self._run_phase(ProjectPhase.QUALITY, self._step_quality, request)
            
            # 10. Certification Engine
            self._run_phase(ProjectPhase.CERTIFICATION, self._step_certification, request)
            
            request.metadata["PROJECT_READY"] = "YES"
            logger.info("===============================================")
            logger.info(f"🏆 PROJECT READY = YES ({request.project_id})")
            logger.info("===============================================")
            
            self.state_manager.complete_project()
            self.state_manager.save_state(request)
            return "SUCCESS"
            
        except Exception as e:
            if self.state_manager.current_phase != ProjectPhase.NEEDS_INPUT:
                self.state_manager.fail_phase(self.state_manager.current_phase, str(e))
                logger.error(f"Pipeline interrompido: {e}")
                request.metadata["PROJECT_READY"] = "NO"
                logger.error("===============================================")
                logger.error(f"❌ PROJECT READY = NO ({request.project_id})")
                logger.error("===============================================")
                self.state_manager.save_state(request)
            return "FAILED"

    def _run_phase(self, phase: ProjectPhase, step_func, request: ProjectRequest) -> bool:
        if self.state_manager.phases[phase].status == PhaseStatus.COMPLETED:
            logger.info(f"[Orchestrator] Fase {phase.name} já concluída, pulando...")
            return True
            
        self.state_manager.transition_to(phase)
        result = step_func(request)
        
        if result is False:
            if phase in [ProjectPhase.EXECUTION, ProjectPhase.VALIDATION]:
                return False
            # O Discovery retorna False se precisar de Input, isso é capturado lá fora
            if phase == ProjectPhase.DISCOVERY and self.state_manager.current_phase == ProjectPhase.NEEDS_INPUT:
                return False
            raise Exception(f"Phase {phase.name} returned failure.")
            
        return result

    def _step_discovery(self, request: ProjectRequest) -> bool:
        logger.info("Executando Discovery...")
        result = self.discovery_agent.run_discovery(request)
        if not result and "missing_info_question" in request.discovery_data:
            self.state_manager.pause_for_input()
        return result

    def _step_dataset_profiling(self, request: ProjectRequest) -> bool:
        logger.info("Executando Dataset Profiling...")
        if request.dataset_path:
            logger.info(f"Analisando dataset em {request.dataset_path}")
            try:
                profile = self.dataset_profiler.profile_dataset(request.dataset_path)
                request.dataset_profile = profile
                if profile.get("status") == "failed":
                    logger.warning(f"Falha ao realizar profiling: {profile.get('error')}")
                else:
                    logger.info(f"Profiling concluído. Encontradas {profile.get('row_count')} linhas e {profile.get('column_count')} colunas.")
            except Exception as e:
                logger.error(f"Erro no Profiling: {str(e)}")
                return False
        return True

    def _step_brain(self, request: ProjectRequest) -> bool:
        logger.info("Executando Brain (Knowledge Retrieval)...")
        return True

    def _step_architecture(self, request: ProjectRequest) -> bool:
        logger.info("Executando Architecture Decisions...")
        return self.architecture_agent.generate_architecture(request)

    def _step_planner(self, request: ProjectRequest) -> bool:
        logger.info("Executando Planner (Project Plan)...")
        return self.planner_agent.generate_plan(request)

    def _step_project_factory(self, request: ProjectRequest) -> bool:
        logger.info("Executando Project Factory...")
        self.compiled_artifacts = self.project_factory.assemble_project(request)
        if not self.compiled_artifacts:
            return False
        return True

    def _step_materialization(self, request: ProjectRequest) -> bool:
        logger.info("Executando Materializer...")
        return self.materializer.materialize(request, self.compiled_artifacts)

    def _step_execution(self, request: ProjectRequest) -> bool:
        logger.info("Executando Execution Runtime...")
        return self.runtime_engine.run_project(request)

    def _step_validation(self, request: ProjectRequest) -> bool:
        logger.info("Executando Validation Gate...")
        return self.validation_gate.run_validation(request)
        
    def _step_repair(self, request: ProjectRequest) -> bool:
        logger.info("Executando Repair Loop...")
        error_context = "Pytest execution failed in validation gate."
        return self.repair_loop.run_repair(request, error_context)

    def _step_quality(self, request: ProjectRequest) -> bool:
        logger.info("Executando Quality Engine...")
        return self.quality_engine.run_quality(request)

    def _step_certification(self, request: ProjectRequest) -> bool:
        logger.info("Executando Certification Engine...")
        return self.certification_engine.run_certification(request)

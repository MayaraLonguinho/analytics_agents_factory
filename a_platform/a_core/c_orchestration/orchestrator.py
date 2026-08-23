import logging
from typing import Any

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.c_orchestration.state_manager import StateManager, ProjectPhase
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
        
        self.compiled_artifacts = []
        
    def execute_pipeline(self, request: ProjectRequest) -> bool:
        self.state_manager = StateManager(request.project_id)
        logger.info(f"Iniciando pipeline para {request.project_id}")
        
        try:
            # Discovery
            self._run_phase(ProjectPhase.DISCOVERY, self._step_discovery, request)
            
            # Dataset Profiling
            self._run_phase(ProjectPhase.DATASET_PROFILING, self._step_dataset_profiling, request)
            
            # Brain
            self._run_phase(ProjectPhase.BRAIN, self._step_brain, request)
            
            # Architecture
            self._run_phase(ProjectPhase.ARCHITECTURE, self._step_architecture, request)
            
            # Planner
            self._run_phase(ProjectPhase.PLANNER, self._step_planner, request)
            
            # Project Factory
            self._run_phase(ProjectPhase.PROJECT_FACTORY, self._step_project_factory, request)
            
            # Materializer
            self._run_phase(ProjectPhase.MATERIALIZATION, self._step_materialization, request)
            
            # Execution & Validation Loop
            validated = False
            while not validated and self.state_manager.repair_attempts <= self.state_manager.max_repair_attempts:
                # Execution Runtime
                self._run_phase(ProjectPhase.EXECUTION, self._step_execution, request)
                
                # Validation Gate
                validation_passed = self._run_phase(ProjectPhase.VALIDATION, self._step_validation, request)
                
                if validation_passed:
                    validated = True
                else:
                    self.state_manager.repair_attempts += 1
                    logger.warning(f"Validation failed. Repair attempt {self.state_manager.repair_attempts}")
                    if self.state_manager.repair_attempts <= self.state_manager.max_repair_attempts:
                        self._run_phase(ProjectPhase.REPAIR_LOOP, self._step_repair, request)
            
            if not validated:
                raise Exception("Validation failed after max repair attempts.")
            
            # Quality Engine
            self._run_phase(ProjectPhase.QUALITY, self._step_quality, request)
            
            # Certification Engine
            self._run_phase(ProjectPhase.CERTIFICATION, self._step_certification, request)
            
            # Conclusão
            self.state_manager.complete_project()
            return True
            
        except Exception as e:
            self.state_manager.fail_phase(self.state_manager.current_phase, str(e))
            logger.error(f"Pipeline interrompido: {e}")
            return False

    def _run_phase(self, phase: ProjectPhase, step_func, request: ProjectRequest) -> Any:
        self.state_manager.transition_to(phase)
        result = step_func(request)
        if result is False: # Explicit failure
            raise Exception(f"Phase {phase.name} returned failure.")
        return result

    def _step_discovery(self, request: ProjectRequest) -> bool:
        logger.info("Executando Discovery...")
        return self.discovery_agent.run_discovery(request)

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
        else:
            logger.info("Nenhum dataset fornecido, pulando profiling...")
        
        return True

    def _step_brain(self, request: ProjectRequest) -> bool:
        logger.info("Executando Brain (Knowledge Retrieval)...")
        logger.info("Brain instanciado e pronto para consultas.")
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
        return True

    def _step_validation(self, request: ProjectRequest) -> bool:
        logger.info("Executando Validation Gate...")
        return True
        
    def _step_repair(self, request: ProjectRequest) -> bool:
        logger.info("Executando Repair Loop...")
        return True

    def _step_quality(self, request: ProjectRequest) -> bool:
        logger.info("Executando Quality Engine...")
        return True

    def _step_certification(self, request: ProjectRequest) -> bool:
        logger.info("Executando Certification Engine...")
        return True

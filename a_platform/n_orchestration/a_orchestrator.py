import logging
import os
from typing import Any, Optional

from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts.f_state_manager import StateManager, ProjectPhase, PhaseStatus
from a_platform.b_contracts import (
    ProjectContext,
    ExecutionResult,
    ValidationResult,
    QualityResult,
    CertificationResult,
)
from a_platform.g_agents.b_discovery.a_discovery_agent import DiscoveryAgent, DiscoveryStatus
from a_platform.e_skills.a_dataset_profiling.c_profiling.a_profiler import DatasetProfilingSkill
from a_platform.c_brain import Brain

from a_platform.g_agents.c_architecture.a_architecture_agent import ArchitectureAgent
from a_platform.c_brain.d_domains.a_domain_registry import DomainRegistry
from a_platform.g_agents.d_planner.k_planner_agent import PlannerAgent
from a_platform.g_agents.n_factory.a_agent_factory import AgentFactory
from a_platform.h_factory import ProjectFactory
from a_platform.h_materializer import ArtifactMaterializer, MaterializationResult
from a_platform.f_mcps.d_registry.b_executor import MCPExecutor
from a_platform.i_llm_gateway.d_gateway import LLMGateway
from a_platform.j_runtime.a_execution.a_runtime import ProjectRuntime
from a_platform.k_validation.a_validation_gate import ValidationGate
from a_platform.l_quality.a_quality_engine import QualityEngine
from a_platform.m_certification.a_certification_engine import CertificationEngine
from a_platform.n_orchestration.c_repair_loop import RepairLoop

logger = logging.getLogger(__name__)


class MasterOrchestrator:
    def __init__(self):
        self.gateway = LLMGateway()
        self.state_manager: Optional[StateManager] = None
        self.mcp = MCPExecutor()
        self.discovery_agent = DiscoveryAgent(gateway=self.gateway)
        self.dataset_profiler = DatasetProfilingSkill()

        self.brain = Brain()
        self.architecture_agent = ArchitectureAgent(self.gateway)
        
        self.domain_registry = DomainRegistry()
        self.planner_agent = PlannerAgent(self.domain_registry)
        self.agent_factory = AgentFactory()
        self.project_factory = ProjectFactory(self.agent_factory)
        self.materializer = ArtifactMaterializer(self.mcp)
        self.runtime_engine = ProjectRuntime()
        self.validation_gate = ValidationGate()
        self.quality_engine = QualityEngine()
        self.certification_engine = CertificationEngine()
        self.repair_loop = RepairLoop(self.agent_factory)
        
        self.compiled_artifacts = []
        self.last_execution_result: Optional[ExecutionResult] = None
        self.last_validation_report: Optional[ValidationResult] = None
        self.last_quality_report: Optional[QualityResult] = None
        self.last_certification_report: Optional[CertificationResult] = None
        
    def execute_pipeline(self, request: ExecutionContext, existing_state: Optional[StateManager] = None) -> str:
        if existing_state:
            self.state_manager = existing_state
            logger.info(f"Retomando pipeline para {request.project_id}")
        else:
            self.state_manager = StateManager(request.project_id)
            logger.info(f"Iniciando novo pipeline para {request.project_id}")
        
        if not hasattr(request, "project_context") or request.project_context is None:
            project_path = os.path.join(os.getcwd(), "e_generated_projects", request.project_id)
            request.project_context = ProjectContext(
                project_id=request.project_id,
                project_name=request.project_id,
                project_path=project_path
            )
            request.project_path = project_path
        
        try:
            # 1. Discovery
            discovery_success = self._run_phase(ProjectPhase.DISCOVERY, self._step_discovery, request)
            if not discovery_success:
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
                            
                    # Remove COMPLETION da execution e validation para rodar novamente
                    self.state_manager.phases[ProjectPhase.EXECUTION].status = PhaseStatus.PENDING
                    self.state_manager.phases[ProjectPhase.VALIDATION].status = PhaseStatus.PENDING
            
            if not validated:
                raise Exception("Validação falhou após o limite máximo de tentativas de reparo.")
            
            # 9. Quality Engine
            self._run_phase(ProjectPhase.QUALITY, self._step_quality, request)
            
            # 10. Certification Engine
            self._run_phase(ProjectPhase.CERTIFICATION, self._step_certification, request)
            
            # 11. Readiness Gate (Regra Absoluta)
            real_exec = self.last_execution_result or ExecutionResult(status="FAILED", error="No execution ran")
            real_val = self.last_validation_report or ValidationResult(status="FAILED", errors=["No validation ran"])
            real_qual = self.last_quality_report or QualityResult(status="FAILED", errors=["No quality ran"])
            real_cert = self.last_certification_report or CertificationResult(status="FAILED", errors=["No certification ran"])
            
            if real_val.status == "PASSED" and real_qual.status == "PASSED" and real_cert.status == "PASSED":
                request.metadata["PROJECT_READY"] = "YES"
                logger.info("===============================================")
                logger.info(f"🏆 PROJECT READY = YES ({request.project_id})")
                logger.info("===============================================")
                self.state_manager.complete_project()
            else:
                raise Exception(
                    f"ReadinessGate rejeitou o projeto por fases incompletas ou com falhas: "
                    f"val={real_val.status}, qual={real_qual.status}, cert={real_cert.status}."
                )
                
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

    def _run_phase(self, phase: ProjectPhase, step_func, request: ExecutionContext) -> bool:
        if self.state_manager.phases[phase].status == PhaseStatus.COMPLETED:
            logger.info(f"[Orchestrator] Fase {phase.name} já concluída, pulando...")
            return True
            
        self.state_manager.transition_to(phase)
        
        try:
            result = step_func(request)
        except Exception as e:
            logger.error(f"[Orchestrator] Fase {phase.name} falhou com exceção: {e}")
            self.state_manager.phases[phase].status = PhaseStatus.FAILED
            raise
            
        if hasattr(result, "status"):
            status_val = str(result.status).upper()
            if status_val in ("FAILED", "ERROR"):
                logger.error(f"[Orchestrator] Fase {phase.name} retornou status de falha: {status_val}")
                self.state_manager.phases[phase].status = PhaseStatus.FAILED
                if phase in [ProjectPhase.EXECUTION, ProjectPhase.VALIDATION, ProjectPhase.REPAIR_LOOP]:
                    return False
                raise Exception(f"Phase {phase.name} returned failure status: {status_val}")
        
        if result is False:
            if phase in [ProjectPhase.EXECUTION, ProjectPhase.VALIDATION, ProjectPhase.REPAIR_LOOP]:
                self.state_manager.phases[phase].status = PhaseStatus.FAILED
                return False
            if phase == ProjectPhase.DISCOVERY and self.state_manager.current_phase == ProjectPhase.NEEDS_INPUT:
                return False
            self.state_manager.phases[phase].status = PhaseStatus.FAILED
            raise Exception(f"Phase {phase.name} returned boolean False.")
            
        self.state_manager.phases[phase].status = PhaseStatus.COMPLETED
        return True

    def _step_discovery(self, request: ExecutionContext) -> bool:
        logger.info("Executando Discovery...")
        import asyncio
        status = asyncio.run(self.discovery_agent.run_discovery(request, self.brain))
        if status == DiscoveryStatus.NEEDS_INPUT:
            self.state_manager.pause_for_input()
            return False
        elif status == DiscoveryStatus.FAILED:
            return False
            
        request.project_type = request.discovery_data.get("project_type")
        request.business_context = request.discovery_data.get("business_context")
        
        # Normalização estrita do domínio após a coleta para garantir 
        # que a Factory e Planner recebam o domínio canônico
        raw_domain = request.discovery_data.get("domain", "")
        normalized_domain = self.domain_registry.normalize_domain(raw_domain)
        
        if normalized_domain not in ["analytics", "data_engineering"]:
            raise ValueError(f"Domínio técnico inválido ou ausente: '{raw_domain}'. Domínios permitidos: 'analytics', 'data_engineering'. Nenhuma interpretação genérica será feita.")

        request.domain = normalized_domain
        request.discovery_data["domain"] = normalized_domain
        if hasattr(request, "project_context") and request.project_context is not None:
            request.project_context.domain = normalized_domain
            
        return True

    def _step_dataset_profiling(self, request: ExecutionContext) -> bool:
        logger.info("Executando Dataset Profiling...")
        if request.dataset_path:
            logger.info(f"Analisando dataset em {request.dataset_path}")
            try:
                result = self.dataset_profiler.execute({"dataset_path": request.dataset_path})
                profile = result.get("dataset_profile", {})
                request.dataset_profile = profile
                
                logger.info(f"Profiling concluído. Encontradas {profile.get('row_count')} linhas e {profile.get('column_count')} colunas.")
            except Exception as e:
                logger.error(f"Erro no Profiling: {str(e)}")
                return False
        return True

    def _step_brain(self, request: ExecutionContext) -> bool:
        logger.info("Executando Brain (Knowledge Retrieval)...")
        context = {
            "project_type": request.project_type,
            "business_context": request.business_context,
            "domain": request.domain,
            "dataset_profile": request.dataset_profile,
            "discovery_data": request.discovery_data
        }
        knowledge = self.brain.retrieve_relevant_knowledge(context)
        request.brain_context = knowledge
        logger.info(f"Conhecimento do Brain injetado no contexto. Padrões: {knowledge.get('domain_patterns')}")
        return True

    def _step_architecture(self, request: ExecutionContext) -> bool:
        logger.info("Executando Architecture Decisions...")
        return self.architecture_agent.generate_architecture(request)

    def _step_planner(self, request: ExecutionContext) -> bool:
        logger.info("Executando Planner (Project Plan)...")
        return self.planner_agent.generate_plan(request)

    def _step_project_factory(self, request: ExecutionContext) -> bool:
        logger.info("Executando Project Factory...")
        self.compiled_artifacts = self.project_factory.generate(request)
        if not self.compiled_artifacts:
            return False
        if hasattr(request, "project_context") and request.project_context is not None:
            request.project_context.generated_artifacts = self.compiled_artifacts
        return True

    def _step_materialization(self, request: ExecutionContext) -> MaterializationResult:
        logger.info("Executando Materializer...")
        result = self.materializer.materialize(request, self.compiled_artifacts)
        if result.status == "PASSED":
            if hasattr(request, "project_context") and request.project_context is not None:
                request.project_context.materialization_status = "SUCCESS"
        else:
            if hasattr(request, "project_context") and request.project_context is not None:
                request.project_context.materialization_status = "FAILED"
            logger.error(f"[Orchestrator] Falha de materialização: {result.evidence}")
            if result.errors:
                logger.error(f"[Orchestrator] Arquivos com falha/ausentes: {result.errors}")
        return result

    def _step_execution(self, request: ExecutionContext) -> bool:
        project_path = request.project_context.project_path if request.project_context else request.project_path
        result = self.runtime_engine.execute(request, project_path=project_path)
        self.last_execution_result = result
        if result.status != "PASSED":
            logger.error(f"Execution failed: {result.evidence}")
        return result.status == "PASSED"

    def _step_validation(self, request: ExecutionContext) -> bool:
        logger.info("Executando Validation Gate...")
        report = self.validation_gate.evaluate(request, self.last_execution_result)
        self.last_validation_report = report
        if report.status != "PASSED":
            logger.error(f"Validation failed. Report: {report.model_dump()}")
        return report.status == "PASSED"
        
    def _step_repair(self, request: ExecutionContext) -> bool:
        logger.info("Executando Repair Loop...")
        val_errors = self.last_validation_report.errors if self.last_validation_report else []
        return self.repair_loop.run_repair(
            request,
            self.last_execution_result,
            validation_errors=val_errors,
            attempt=self.state_manager.repair_attempts
        )

    def _step_quality(self, request: ExecutionContext) -> bool:
        logger.info("Executando Quality Engine...")
        
        exec_obj = self.last_execution_result if self.last_execution_result else None
        val_obj = self.last_validation_report if self.last_validation_report else None
        
        report = self.quality_engine.evaluate(
            request, 
            validation_result=val_obj, 
            runtime_result=exec_obj
        )
        self.last_quality_report = report
        if report.status != "PASSED":
            logger.error(f"Quality failed. Report: {report.model_dump()}")
        return report.status == "PASSED"

    def _step_certification(self, request: ExecutionContext) -> bool:
        logger.info("Executando Certification Engine...")
        
        exec_obj = self.last_execution_result if self.last_execution_result else None
        val_obj = self.last_validation_report if self.last_validation_report else None
        qual_obj = self.last_quality_report if self.last_quality_report else None
        
        report = self.certification_engine.evaluate(
            request,
            execution_result=exec_obj,
            validation_result=val_obj,
            quality_result=qual_obj
        )
        self.last_certification_report = report
        if report.status != "PASSED":
            logger.error(f"Certification failed. Report: {report.model_dump()}")
        return report.status == "PASSED"

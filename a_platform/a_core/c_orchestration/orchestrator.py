import asyncio
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.c_orchestration.state_manager import StateManager
from c_agents.a_discovery_agent.discovery_agent import DiscoveryAgent
from c_agents.b_architecture_agent.architecture_agent import ArchitectureAgent
from c_agents.c_planner_agent.planner_agent import PlannerAgent
from c_agents.d_etl_agent.etl_agent import ETLAgent
from c_agents.e_db_agent.db_agent import DBAgent
from c_agents.f_backend_agent.backend_agent import BackendAgent
from c_agents.g_frontend_agent.frontend_agent import FrontendAgent
from c_agents.h_devops_agent.devops_agent import DevOpsAgent
from c_agents.i_qa_agent.qa_agent import QAAgent
from c_agents.j_documentation_agent.doc_agent import DocumentationAgent
from a_platform.g_materializer.materializer import Materializer
from a_platform.h_runtime.runtime_engine import RuntimeEngine
from a_platform.i_validation.validation_gate import ValidationGate
from a_platform.k_certification.certification_engine import CertificationEngine
from a_platform.j_quality.quality_engine import QualityEngine
from a_platform.m_learning.learning_engine import LearningEngine
from a_platform.b_brain.g_graph.obsidian.graph_builder import ObsidianGraphBuilder

class MasterOrchestrator:
    def __init__(self):
        self.state = StateManager()
        self.discovery = DiscoveryAgent()
        self.architecture = ArchitectureAgent()
        self.planner = PlannerAgent()
        self.specialists = {
            "etl_pipeline": ETLAgent(),
            "db_setup": DBAgent(),
            "backend_api": BackendAgent(),
            "frontend_dashboard": FrontendAgent(),
            "devops_infra": DevOpsAgent(),
            "qa_tests": QAAgent()
        }
        self.doc_agent = DocumentationAgent()
        self.materializer = Materializer()
        self.runtime = RuntimeEngine()
        self.validation = ValidationGate()
        self.quality = QualityEngine()
        self.certification = CertificationEngine()
        self.learning = LearningEngine()
        self.graph_builder = ObsidianGraphBuilder(output_dir="e_generated_projects/.obsidian_graph")
        self.max_repairs = 3

    async def run_pipeline(self, prompt: str):
        self.state.update("prompt", prompt)
        self.state.update("status", "DISCOVERY")
        
        try:
            request = ProjectRequest(request=prompt, domain="generic", source="cli")
            discovery_result = await self.discovery.execute(request)
            
            plan = await self.architecture.execute(discovery_result)
            self.state.update("project_plan", plan)
            
            # Generate Obsidian Graph
            nodes = [{"id": f"Phase_{phase.name}", "content": phase.description} for phase in plan.phases]
            self.graph_builder.build_graph(nodes)
            
            self.state.update("status", "PLANNING")
            plan = await self.planner.execute(plan)
            
            attempt = 0
            success = False
            
            while attempt < self.max_repairs and not success:
                self.state.update("status", f"FACTORY_ATTEMPT_{attempt+1}")
                artifacts = []
                for task in plan.tasks:
                    if task in self.specialists:
                        agent = self.specialists[task]
                        artifact = await agent.execute(task)
                        artifacts.append(artifact)
                        
                self.state.update("status", f"DOCUMENTING_ATTEMPT_{attempt+1}")
                doc_artifact = await self.doc_agent.execute(plan, artifacts)
                artifacts.append(doc_artifact)
                
                self.state.update("artifacts", artifacts)
                
                self.state.update("status", f"MATERIALIZING_ATTEMPT_{attempt+1}")
                project_dir = self.materializer.materialize(plan.project_id, artifacts)
                self.state.update("project_dir", project_dir)
                
                self.state.update("status", f"RUNTIME_ATTEMPT_{attempt+1}")
                runtime_ok = self.runtime.execute_real(project_dir)
                
                self.state.update("status", f"VALIDATION_ATTEMPT_{attempt+1}")
                val_result = self.validation.validate(project_dir)
                
                if runtime_ok and val_result["is_valid"]:
                    success = True
                else:
                    attempt += 1
                    self.learning.record_failure(plan.project_id, val_result)
                    
            self.state.update("status", "CERTIFICATION")
            cert = self.certification.certify_project(plan.project_id, project_dir)
            self.state.update("certification", cert)
            
            is_ready = success and cert.is_certified
            
            if is_ready:
                self.state.update("status", "COMPLETED_SUCCESS")
            else:
                self.state.update("status", "COMPLETED_REJECTED")
                
            return self.state
            
        except Exception as e:
            self.state.update("status", "FAILED")
            return self.state

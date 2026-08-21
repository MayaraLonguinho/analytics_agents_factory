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
from a_platform.g_materializer.materializer import Materializer
from a_platform.h_runtime.runtime_engine import RuntimeEngine
from a_platform.k_certification.certification_engine import CertificationEngine

class MasterOrchestrator:
    def __init__(self):
        self.state = StateManager()
        # Motores & Agentes
        self.discovery = DiscoveryAgent()
        self.architecture = ArchitectureAgent()
        self.planner = PlannerAgent()
        
        # Factory
        self.specialists = {
            "etl_pipeline": ETLAgent(),
            "db_setup": DBAgent(),
            "backend_api": BackendAgent(),
            "frontend_dashboard": FrontendAgent(),
            "devops_infra": DevOpsAgent(),
            "qa_tests": QAAgent()
        }
        
        self.materializer = Materializer()
        self.runtime = RuntimeEngine()
        self.certification = CertificationEngine()

    async def run_pipeline(self, prompt: str):
        self.state.update("prompt", prompt)
        self.state.update("status", "DISCOVERY")
        
        try:
            # 1. Discovery
            request = ProjectRequest(request=prompt, domain="generic", source="cli")
            discovery_result = await self.discovery.execute(request)
            
            # 2. Architecture
            plan = await self.architecture.execute(discovery_result)
            self.state.update("project_plan", plan)
            
            # 3. Planner
            self.state.update("status", "PLANNING")
            plan = await self.planner.execute(plan)
            
            # 4. Factory
            self.state.update("status", "FACTORY")
            artifacts = []
            for task in plan.tasks:
                if task in self.specialists:
                    agent = self.specialists[task]
                    artifact = await agent.execute(task)
                    artifacts.append(artifact)
            self.state.update("artifacts", artifacts)
            
            # 5. Materializer
            self.state.update("status", "MATERIALIZING")
            project_dir = self.materializer.materialize(plan.project_id, artifacts)
            self.state.update("project_dir", project_dir)
            
            # 6. Runtime
            self.state.update("status", "RUNTIME")
            self.runtime.run_project(project_dir)
            
            # 7. Certification
            self.state.update("status", "CERTIFICATION")
            cert = self.certification.certify_project(plan.project_id, project_dir)
            self.state.update("certification", cert)
            
            if cert.is_certified:
                self.state.update("status", "COMPLETED_SUCCESS")
            else:
                self.state.update("status", "COMPLETED_REJECTED")
                
            return self.state
            
        except Exception as e:
            raise e
            return self.state

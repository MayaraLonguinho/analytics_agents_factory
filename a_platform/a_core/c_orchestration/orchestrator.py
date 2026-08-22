import asyncio
import os
import sys
import subprocess
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.c_orchestration.state_manager import StateManager
from a_platform.c_agents.b_discovery.discovery_agent import DiscoveryAgent
from a_platform.d_skills.d_data_engineering.profiler import DataProfilerSkill
from a_platform.c_agents.c_architecture.architecture_agent import ArchitectureAgent
from a_platform.c_agents.d_planner.planner_agent import PlannerAgent
from a_platform.g_factory.a_project_factory.project_factory import ProjectFactory
from a_platform.g_factory.d_artifact_materializer.materializer import Materializer
from a_platform.i_runtime.a_runtime import RuntimeEngine
from a_platform.j_validation.a_validation_gate import ValidationGate
from a_platform.k_quality.a_quality_engine import QualityEngine
from a_platform.l_certification.a_certification_engine import CertificationEngine
from a_platform.m_learning.a_learning_engine import LearningEngine
from a_platform.b_brain.g_graph.obsidian.graph_builder import ObsidianGraphBuilder

class MasterOrchestrator:
    def __init__(self):
        self.state = StateManager()
        self.discovery = DiscoveryAgent()
        self.profiler = DataProfilerSkill()
        self.architecture = ArchitectureAgent()
        self.planner = PlannerAgent()
        self.factory = ProjectFactory()
        self.materializer = Materializer()
        self.runtime = RuntimeEngine()
        self.validation = ValidationGate()
        self.quality = QualityEngine()
        self.certification = CertificationEngine()
        self.learning = LearningEngine()
        self.graph_builder = ObsidianGraphBuilder(output_dir="e_generated_projects/.obsidian_graph")
        self.max_repairs = 3

    def run_pipeline(self, prompt: str, dataset_path: str = None):
        return asyncio.run(self.run_pipeline_async(prompt, dataset_path))

    async def run_pipeline_async(self, prompt: str, dataset_path: str = None):
        print(f"\\n=== Iniciando AAF Pipeline v1.0 ===")
        print(f"-> Prompt: {prompt}\\n")
        
        self.state.update("prompt", prompt)
        
        # 1. DISCOVERY
        self.state.update("status", "DISCOVERY")
        print("[1/10] Executando Discovery Agent...")
        request = ProjectRequest(request=prompt, domain="analytics" if "dados" in prompt.lower() or "etl" in prompt.lower() else "generic", source="cli")
        discovery_result = await self.discovery.execute(request)
        
        # 2. PROFILING (se dataset fornecido)
        profiling_data = {}
        if dataset_path and os.path.exists(dataset_path):
            self.state.update("status", "PROFILING")
            print(f"[2/10] Executando Dataset Profiling em {dataset_path}...")
            profiling_data = self.profiler.profile_dataset(dataset_path)
        else:
            print("[2/10] Dataset Profiling: Ignorado (Nenhum dataset fornecido)")
            
        # 3. BRAIN & ARCHITECTURE
        print("[3/10] Consultando Brain & Desenhando Arquitetura...")
        plan = await self.architecture.execute(discovery_result) # simplificado para reuso de schema
        self.state.update("project_plan", plan)
        
        nodes = [{"id": f"Phase_{phase.name}", "content": phase.description} for phase in plan.phases]
        self.graph_builder.build_graph(nodes)
        
        # 4. PLANNER
        self.state.update("status", "PLANNING")
        print("[4/10] Executando Project Planner...")
        plan = await self.planner.execute(plan)
        
        # 5. FACTORY & MATERIALIZATION & REPAIR LOOP
        attempt = 0
        success = False
        project_dir = ""
        
        while attempt < self.max_repairs and not success:
            print(f"\\n--- Tentativa {attempt + 1} de {self.max_repairs} ---")
            
            # FACTORY
            self.state.update("status", f"FACTORY_ATTEMPT_{attempt+1}")
            print("[5/10] Factory Agent: Coordenando a geração de código via LLM/Agents...")
            artifacts = await self.factory.generate_project(plan, discovery_result, profiling_data)
            self.state.update("artifacts", artifacts)
            
            # MATERIALIZATION
            self.state.update("status", f"MATERIALIZING_ATTEMPT_{attempt+1}")
            print("[6/10] Materializer: Gravando arquivos físicos no disco...")
            # We override project_id logic slightly for cleaner folders
            project_id = plan.project_id if hasattr(plan, "project_id") else "arch-plan-001"
            domain_folder = discovery_result.domain if hasattr(discovery_result, "domain") else "generic"
            # Ensure proper path
            import uuid
            unique_id = str(uuid.uuid4())[:8]
            project_id = f"{domain_folder}-{unique_id}"
            
            # Manually materialize to ensure proper directory
            project_dir = os.path.abspath(f"e_generated_projects/{domain_folder}/{project_id}")
            os.makedirs(project_dir, exist_ok=True)
            for artifact in artifacts:
                filepath = os.path.join(project_dir, artifact.path)
                with open(filepath, "w") as f:
                    f.write(artifact.content)
                    
            self.state.update("project_dir", project_dir)
            
            # RUNTIME
            self.state.update("status", f"RUNTIME_ATTEMPT_{attempt+1}")
            print("[7/10] Execution Runtime: Instanciando projeto (venv, pip install, execução)...")
            runtime_ok = self.runtime.execute_real(project_dir)
            
            # VALIDATION
            self.state.update("status", f"VALIDATION_ATTEMPT_{attempt+1}")
            print("[8/10] Validation Gate: Rodando suíte de testes isolada...")
            val_result = self.validation.validate(project_dir)
            
            if runtime_ok and val_result["is_valid"]:
                print("  [Validation] Sucesso!")
                success = True
            else:
                print("  [Validation] Falha detectada. Acionando Repair Loop e Learning Engine...")
                attempt += 1
                self.learning.record_failure(project_id, {"error": val_result["error_payload"]})
                
        # QUALITY & CERTIFICATION
        self.state.update("status", "CERTIFICATION")
        print("\\n[9/10] Quality Engine: Realizando linting estático...")
        q_result = self.quality.run_checks(project_dir)
        
        print("[10/10] Certification Engine: Avaliando métricas e score...")
        cert = self.certification.certify_project(project_id, project_dir)
        self.state.update("certification", cert)
        
        is_ready = success and cert.is_certified and q_result
        
        if is_ready:
            print("\\n========================================================")
            print(f" 🏭 PROJECT READY = YES | ID: {project_id}")
            print("========================================================")
            self.state.update("status", "COMPLETED_SUCCESS")
        else:
            print("\\n========================================================")
            print(" 🏭 PROJECT READY = NO")
            print("========================================================")
            self.state.update("status", "COMPLETED_REJECTED")
            
        return self.state

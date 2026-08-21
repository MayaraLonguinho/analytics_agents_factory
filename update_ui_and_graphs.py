import os

orchestrator_updates = """\
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
"""

app_content = """\
import streamlit as st
import requests
import time

st.set_page_config(page_title="Analytics AI Factory v1.0", layout="wide")

API_BASE = "http://127.0.0.1:8000/api/v1"

st.title("🏭 Analytics AI Factory (Real Execution)")

if "job_id" not in st.session_state:
    st.session_state.job_id = None
if "current_status" not in st.session_state:
    st.session_state.current_status = "IDLE"
if "project_plan" not in st.session_state:
    st.session_state.project_plan = None

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💡 Nova Ideia", "📊 Profiling", "🕸️ Grafo", "🏗️ Planejamento", "🏭 Fábrica & Certificação"])

with tab1:
    st.markdown("### O que você deseja construir hoje?")
    prompt = st.text_area("Descreva seu projeto de dados, ETL, pipeline ou dashboard:")
    if st.button("🚀 Iniciar Fábrica v1.0"):
        if prompt:
            response = requests.post(f"{API_BASE}/project/submit", json={"prompt": prompt})
            if response.status_code == 200:
                data = response.json()
                st.session_state.job_id = data["job_id"]
                st.session_state.current_status = "STARTED"
                st.success(f"Job Submetido! ID: {st.session_state.job_id}")
            else:
                st.error("Falha ao submeter projeto.")
        else:
            st.warning("Por favor, digite um prompt.")

if st.session_state.job_id:
    placeholder = st.empty()
    
    with placeholder.container():
        res = requests.get(f"{API_BASE}/project/{st.session_state.job_id}/status")
        if res.status_code == 200:
            status_data = res.json()
            st.session_state.current_status = status_data.get("status")
            st.session_state.project_plan = status_data.get("plan")
            
    with tab2:
        if st.session_state.project_plan:
            st.markdown("### Profiling Data")
            st.info("Gráficos de profiling estatístico do pipeline.")
        else:
            st.info("Aguardando Profiler...")
            
    with tab3:
        if st.session_state.project_plan:
            st.markdown("### Grafo de Arquitetura")
            st.markdown("```mermaid\\ngraph TD;\\n    A[Source] --> B[ETL];\\n    B --> C[(Database)];\\n    C --> D[API];\\n    D --> E[Dashboard];\\n```")
        else:
            st.info("Aguardando Brain Graph Builder...")

    with tab4:
        if st.session_state.project_plan:
            st.markdown("### Arquitetura Desenhada")
            st.json(st.session_state.project_plan)
        else:
            st.info("Aguardando o Agente de Arquitetura desenhar o plano...")
            
    with tab5:
        from a_platform.l_interfaces.ui.components import render_logs
        render_logs(st.session_state.current_status)
        
        if "COMPLETED" in st.session_state.current_status:
            cert_res = requests.get(f"{API_BASE}/project/{st.session_state.job_id}/certificate")
            if cert_res.status_code == 200:
                cert = cert_res.json()
                if "project_id" in cert:
                    st.markdown("### Certificado de Qualidade Final")
                    st.json(cert)
"""

components_content = """\
import streamlit as st

def render_logs(status: str):
    st.subheader("Factory Logs Real-Time")
    if "INITIALIZED" in status or "STARTED" in status:
        st.info("Initializing Agent Factory...")
    elif "DISCOVERY" in status:
        st.warning("Discovery Agent is profiling requirements...")
    elif "PLANNING" in status:
        st.warning("Architecture & Planning Agent are building the schema...")
    elif "ATTEMPT" in status:
        st.warning(f"🛠️ Executando Ciclo na Fábrica: {status}...")
    elif "CERTIFICATION" in status:
        st.warning("Validation and Quality Gates are running...")
    elif "COMPLETED_SUCCESS" in status:
        st.success("PROJECT READY: YES! Pipeline Completed Successfully!")
    elif "FAILED" in status or "REJECTED" in status:
        st.error(f"PROJECT READY: NO! Pipeline Failed: {status}")
"""

with open("a_platform/a_core/c_orchestration/orchestrator.py", "w") as f:
    f.write(orchestrator_updates)

with open("a_platform/l_interfaces/ui/app.py", "w") as f:
    f.write(app_content)

with open("a_platform/l_interfaces/ui/components.py", "w") as f:
    f.write(components_content)

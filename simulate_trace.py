import sys
from unittest.mock import patch, MagicMock

sys.modules['a_platform.g_llm_gateway.gateway'] = MagicMock()
sys.modules['a_platform.d_agents.agent_factory'] = MagicMock()
sys.modules['a_platform.h_factory.a_project_factory.project_factory'] = MagicMock()

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.c_orchestration.orchestrator import MasterOrchestrator
from a_platform.d_agents.b_discovery.discovery_agent import DiscoveryStatus

def run_evidence_trace():
    print("\n--- SIMULAÇÃO DE ORDEM DAS FASES (EVIDÊNCIA ESTRUTURADA) ---")
    orchestrator = MasterOrchestrator()
    request = ProjectRequest(prompt="Simulate project", project_id="proj_evidence")
    
    # Setup happy path for all steps
    orchestrator.discovery_agent.run_discovery = MagicMock(return_value=DiscoveryStatus.COMPLETE)
    request.discovery_data = {"project_type": "Data Pipeline", "business_context": "finance", "domain": "analytics"}
    
    orchestrator.dataset_profiler.execute = MagicMock(return_value={"dataset_profile": {}})
    orchestrator.brain.retrieve_relevant_knowledge = MagicMock(return_value={})
    orchestrator.architecture_agent.generate_architecture = MagicMock(return_value=True)
    orchestrator.planner_agent.generate_plan = MagicMock(return_value=True)
    orchestrator.project_factory.assemble_project = MagicMock(return_value=["mock_artifact"])
    orchestrator.materializer.materialize = MagicMock(return_value=True)
    orchestrator.runtime_engine.run_project = MagicMock(return_value=True)
    orchestrator.validation_gate.run_validation = MagicMock(return_value=True)
    orchestrator.quality_engine.run_quality = MagicMock(return_value=True)
    orchestrator.certification_engine.run_certification = MagicMock(return_value=True)
    
    result = orchestrator.execute_pipeline(request)
    
    print("\n[RESUMO DO PIPELINE EXECUTADO (Ordem cronológica)]: ")
    phases = orchestrator.state_manager.phases
    for name, phase_obj in phases.items():
        if phase_obj.status.name == "COMPLETED":
            print(f" -> {name}")
            
    print(f"\nResultado Final: {result}")
    print(f"Project Ready: {request.metadata.get('PROJECT_READY')}")
    print("----------------------------------------------------------\n")

if __name__ == "__main__":
    run_evidence_trace()

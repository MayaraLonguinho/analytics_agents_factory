import pytest
from a_platform.a_core.c_orchestration.orchestrator import MasterOrchestrator
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.d_agents.b_discovery.discovery_agent import DiscoveryStatus

class MockDiscoveryAgent:
    def __init__(self, mock_data):
        self.mock_data = mock_data
    def run_discovery(self, request):
        request.discovery_data.update(self.mock_data)
        return DiscoveryStatus.COMPLETE

def test_orchestrator_semantic_resolution_etl_vendas():
    orchestrator = MasterOrchestrator()
    request = ProjectRequest(prompt="test", project_id="test_id")
    
    # Simula LLM se confundindo
    orchestrator.discovery_agent = MockDiscoveryAgent({
        "project_type": "ETL",
        "business_context": "vendas",
        "domain": "vendas" # Assunto sendo passado como domínio
    })
    
    # Orquestrador recebe request crua e recria state manager
    import a_platform.a_core.c_orchestration.state_manager as sm
    orchestrator.state_manager = sm.StateManager("test_id")
    
    success = orchestrator._step_discovery(request)
    assert success is True
    
    # O domínio final deve ser data_engineering!
    assert request.discovery_data["domain"] == "data_engineering"

def test_orchestrator_semantic_resolution_analytics():
    orchestrator = MasterOrchestrator()
    request = ProjectRequest(prompt="test", project_id="test_id")
    
    orchestrator.discovery_agent = MockDiscoveryAgent({
        "project_type": "Dashboard Analítico",
        "business_context": "RH",
        "domain": "analytics" # LLM acertou o domínio
    })
    
    import a_platform.a_core.c_orchestration.state_manager as sm
    orchestrator.state_manager = sm.StateManager("test_id")
    
    success = orchestrator._step_discovery(request)
    assert success is True
    
    # O domínio final deve continuar sendo analytics
    assert request.discovery_data["domain"] == "analytics"

def test_orchestrator_unknown_domain():
    orchestrator = MasterOrchestrator()
    request = ProjectRequest(prompt="test", project_id="test_id")
    
    orchestrator.discovery_agent = MockDiscoveryAgent({
        "project_type": "Sistema X",
        "business_context": "Financeiro",
        "domain": "financeiro" # Não existe domínio financeiro nem alias 'Sistema X'
    })
    
    import a_platform.a_core.c_orchestration.state_manager as sm
    orchestrator.state_manager = sm.StateManager("test_id")
    
    success = orchestrator._step_discovery(request)
    assert success is True
    
    # O domínio final continuará sendo 'financeiro', que falhará no get_domain_config (como esperado)
    assert request.discovery_data["domain"] == "financeiro"

import pytest
from unittest.mock import patch, MagicMock

from a_platform.a_interfaces.ide.adapter import IDEAdapter
from a_platform.a_interfaces.ide.session import IDESession

@patch('a_platform.c_agents.b_discovery.discovery_agent.LLMGateway')
def test_discovery_session_pauses_and_continues(MockGateway):
    mock_llm = MagicMock()
    MockGateway.return_value = mock_llm

    # Primeira chamada: simula retorno faltando informações (NEEDS_INPUT)
    mock_llm.generate_text.return_value = {
        "success": True,
        "text": '''
        {
          "domain": "Analytics",
          "objective": null,
          "users": null,
          "data_sources": null,
          "functional_requirements": null,
          "technical_requirements": null,
          "database": null,
          "backend": null,
          "frontend": null,
          "infrastructure": null,
          "testing": null,
          "documentation": null,
          "constraints": null,
          "missing_info_question": "Qual é o objetivo principal do sistema?"
        }
        '''
    }

    adapter = IDEAdapter()
    res = adapter.create_project("Crie um sistema")
    
    assert res.success is True
    assert res.status == "NEEDS_INPUT"
    assert res.message == "Qual é o objetivo principal do sistema?"
    
    project_id = res.project_id
    
    # Segunda chamada: simula que o LLM agora achou tudo, sem pergunta
    mock_llm.generate_text.return_value = {
        "success": True,
        "text": '''
        {
          "domain": "Analytics",
          "objective": "Analisar vendas",
          "users": "Admins",
          "data_sources": "PostgreSQL",
          "functional_requirements": "Dashboard",
          "technical_requirements": "Python 3.10",
          "database": "PostgreSQL",
          "backend": "FastAPI",
          "frontend": "Streamlit",
          "infrastructure": "Docker",
          "testing": "Pytest",
          "documentation": "Swagger",
          "constraints": "Nenhuma",
          "missing_info_question": null
        }
        '''
    }
    
    # Patch the rest of the orchestration so it doesn't fail on subsequent phases
    # we just want to see if the state manager transitions correctly past NEEDS_INPUT.
    # To do this safely without mocking everything, we can just intercept the orchestrator
    # or just let it fail at another phase and assert it moved past NEEDS_INPUT.
    
    with patch('a_platform.a_core.c_orchestration.orchestrator.MasterOrchestrator._step_dataset_profiling', return_value=True), \
         patch('a_platform.a_core.c_orchestration.orchestrator.MasterOrchestrator._step_brain', return_value=True), \
         patch('a_platform.a_core.c_orchestration.orchestrator.MasterOrchestrator._step_architecture', return_value=True), \
         patch('a_platform.a_core.c_orchestration.orchestrator.MasterOrchestrator._step_planner', return_value=False): # Force fail at planner just to exit loop quickly
        
        # O usuário responde a pergunta
        res2 = adapter.continue_project(project_id, "O objetivo é analisar vendas")
        
        # O pipeline deve falhar agora (porque mockamos o planner pra retornar False para sair cedo)
        # Mas o importante é que NÃO É NEEDS_INPUT
        assert res2.status == "FAILED"
        assert res2.project_id == project_id
        
        # O state manager deve estar salvo com os novos dados do discovery
        state_manager, request = IDESession.load_session(project_id)
        assert request.discovery_data.get("objective") == "Analisar vendas"
        assert request.discovery_data.get("status") == "COMPLETE"

# pyrefly: ignore [missing-import]
from unittest.mock import patch
from a_platform.b_interfaces.a_ide.adapter import IDEAdapter
from c_tests.end_to_end.mock_gateway import get_mocked_generate_function

def setup_ide_adapter():
    adapter = IDEAdapter()
    return adapter

def test_runtime_failure_blocks_readiness():
    adapter = setup_ide_adapter()
    mock_func = get_mocked_generate_function(interactive=False, repair_error=False)
    
    with patch("a_platform.g_llm_gateway.gateway.LLMGateway.generate", side_effect=mock_func), \
         patch("a_platform.j_runtime.runtime_engine.RuntimeEngine.run_project", return_value=False):
         
        response = adapter.create_project("Test runtime failure", domain="analytics")
        
        assert response.success is False
        assert response.status == "FAILED"
        
        # O projeto não deve estar pronto
        status_resp = adapter.get_project_result(response.project_id)
        assert status_resp.status != "READY"

def test_validation_failure_blocks_readiness():
    adapter = setup_ide_adapter()
    mock_func = get_mocked_generate_function(interactive=False, repair_error=False)
    
    with patch("a_platform.g_llm_gateway.gateway.LLMGateway.generate", side_effect=mock_func), \
         patch("a_platform.k_validation.validation_gate.ValidationGate.run_validation", return_value=False):
         
        response = adapter.create_project("Test validation failure", domain="analytics")
        
        assert response.success is False
        assert response.status == "FAILED"
        
        # O projeto não deve estar pronto
        status_resp = adapter.get_project_result(response.project_id)
        assert status_resp.status != "READY"

def test_certification_failure_blocks_readiness():
    adapter = setup_ide_adapter()
    mock_func = get_mocked_generate_function(interactive=False, repair_error=False)
    
    with patch("a_platform.g_llm_gateway.gateway.LLMGateway.generate", side_effect=mock_func), \
         patch("a_platform.m_certification.certification_engine.CertificationEngine.run_certification", return_value=False):
         
        response = adapter.create_project("Test certification failure", domain="analytics")
        
        assert response.success is False
        assert response.status == "FAILED"
        
        # O projeto não deve estar pronto
        status_resp = adapter.get_project_result(response.project_id)
        assert status_resp.status != "READY"

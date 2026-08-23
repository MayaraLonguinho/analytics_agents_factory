import pytest
from unittest.mock import MagicMock, patch
import os
import shutil

from a_platform.a_interfaces.ide.adapter import IDEAdapter
from a_platform.a_core.c_orchestration.orchestrator import MasterOrchestrator
from a_platform.c_agents.agent_factory import AgentFactory

@pytest.fixture
def mock_gateway():
    with patch("a_platform.f_llm_gateway.gateway.LLMGateway.generate_text") as mock_generate:
        # Mocking generic success response
        mock_generate.return_value = {
            "success": True, 
            "text": "```json\n{\"file_name\": \"test.py\", \"fixed_content\": \"def test(): pass\", \"agent_type\": \"testingagent\"}\n```"
        }
        yield mock_generate

@pytest.fixture
def setup_teardown_projects():
    # Setup
    test_proj_dir = os.path.join(os.getcwd(), "e_generated_projects", "analytics", "e2e_test_proj")
    os.makedirs(test_proj_dir, exist_ok=True)
    
    with open(os.path.join(test_proj_dir, "test.py"), "w") as f:
        f.write('"""Docstring"""\ndef test(): pass')
        
    yield test_proj_dir
    
    # Teardown
    if os.path.exists(test_proj_dir):
        shutil.rmtree(test_proj_dir)

def test_full_pipeline_success(mock_gateway, setup_teardown_projects):
    """
    Testa o fluxo completo do orchestrator via IDEAdapter
    simulando aprovação de todas as etapas e garantindo PROJECT_READY=YES.
    """
    adapter = IDEAdapter()
    
    with patch.object(MasterOrchestrator, '_step_discovery', return_value=True), \
         patch.object(MasterOrchestrator, '_step_dataset_profiling', return_value=True), \
         patch.object(MasterOrchestrator, '_step_brain', return_value=True), \
         patch.object(MasterOrchestrator, '_step_architecture', return_value=True), \
         patch.object(MasterOrchestrator, '_step_planner', return_value=True), \
         patch.object(MasterOrchestrator, '_step_project_factory', return_value=True), \
         patch.object(MasterOrchestrator, '_step_materialization', return_value=True), \
         patch.object(MasterOrchestrator, '_step_execution', return_value=True), \
         patch.object(MasterOrchestrator, '_step_validation', return_value=True), \
         patch.object(MasterOrchestrator, '_step_quality', return_value=True), \
         patch.object(MasterOrchestrator, '_step_certification', return_value=True):
         
        # Cria projeto
        res = adapter.create_project("Quero um projeto de analytics simples", "e2e_test_proj")
        
        # Como o discovery e as outras etapas mockadas retornaram True,
        # o orquestrador vai rodar até o final
        
        assert getattr(res, "status", None) == "READY", f"Pipeline failed: {res}"
        
        # Verifica se Project Ready = YES
        from a_platform.a_interfaces.ide.session import IDESession
        state_manager, request = IDESession.load_session(res.project_id)
        assert request.metadata.get("PROJECT_READY") == "YES"

def test_pipeline_with_repair_loop(mock_gateway, setup_teardown_projects):
    """
    Testa se o Repair Loop é ativado quando Validation falha
    e se ele conserta e avança.
    """
    adapter = IDEAdapter()
    
    # Simulamos execution sucesso, mas validation falha na primeira tentativa e passa na segunda
    validation_side_effect = [False, True]
    
    with patch.object(MasterOrchestrator, '_step_discovery', return_value=True), \
         patch.object(MasterOrchestrator, '_step_dataset_profiling', return_value=True), \
         patch.object(MasterOrchestrator, '_step_brain', return_value=True), \
         patch.object(MasterOrchestrator, '_step_architecture', return_value=True), \
         patch.object(MasterOrchestrator, '_step_planner', return_value=True), \
         patch.object(MasterOrchestrator, '_step_project_factory', return_value=True), \
         patch.object(MasterOrchestrator, '_step_materialization', return_value=True), \
         patch.object(MasterOrchestrator, '_step_execution', return_value=True), \
         patch.object(MasterOrchestrator, '_step_quality', return_value=True), \
         patch.object(MasterOrchestrator, '_step_certification', return_value=True), \
         patch('a_platform.j_validation.validation_gate.ValidationGate.run_validation', side_effect=validation_side_effect):
         
        # Simulamos que repair passará
        with patch.object(MasterOrchestrator, '_step_repair', return_value=True):
            res = adapter.create_project("Quero analytics e vai falhar", "e2e_test_proj")
            
            assert getattr(res, "status", None) == "READY", f"Pipeline failed: {res}"
            
            # The IDEAdapter creates a new orchestrator, so the state manager is not on the adapter.
            # But the session gets saved, we can load it.
            from a_platform.a_interfaces.ide.session import IDESession
            state_manager, request = IDESession.load_session(res.project_id)
            assert state_manager.repair_attempts == 1
            assert request.metadata.get("PROJECT_READY") == "YES"

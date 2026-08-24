import pytest
import os
import shutil
from unittest.mock import patch
from a_platform.b_interfaces.a_ide.adapter import IDEAdapter
from c_tests.end_to_end.mock_gateway import get_mocked_generate_function

def test_ide_interactive_session_e2e():
    """
    Simula o usuário fornecendo um prompt incompleto,
    recebendo 'NEEDS_INPUT' e respondendo no chat para concluir.
    """
    adapter = IDEAdapter()
    
    mock_func = get_mocked_generate_function(interactive=True, repair_error=False)
    
    with patch("a_platform.g_llm_gateway.gateway.LLMGateway.generate", side_effect=mock_func):
        prompt = "Analise."
        
        # Passo 1: O sistema deve pedir mais inputs (is_complete = false mockado)
        response1 = adapter.create_project(prompt, domain="analytics")
        
        assert response1.success is True
        assert response1.status == "NEEDS_INPUT"
        assert "Qual o domínio do projeto?" in response1.message
        
        project_id = response1.project_id
        
        # Passo 2: O usuário responde (is_complete = true mockado na segunda chamada)
        response2 = adapter.continue_project(project_id, "O domínio é analytics")
        
        # O Pipeline deve fluir agora
        assert response2.success is True
        assert response2.status == "READY"
        assert response2.project_id == project_id
        
        # Verificar arquivos
        gen_path = os.path.join("e_generated_projects", "analytics", project_id)
        assert os.path.exists(gen_path)
        assert os.path.exists(os.path.join(gen_path, "main.py"))
        
        # Limpeza
        shutil.rmtree(gen_path, ignore_errors=True)

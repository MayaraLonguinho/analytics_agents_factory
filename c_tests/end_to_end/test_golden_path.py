import pytest
import os
import shutil
from unittest.mock import patch
from a_platform.a_interfaces.ide.adapter import IDEAdapter
from c_tests.end_to_end.mock_gateway import get_mocked_generate_function

def test_golden_path_e2e():
    """
    Simula uma requisição ponta a ponta que dá certo na primeira vez.
    Nenhum erro de dependência, código perfeito, qualidade boa, certificação aprovada.
    """
    adapter = IDEAdapter()
    
    mock_func = get_mocked_generate_function(interactive=False, repair_error=False)
    
    with patch("a_platform.f_llm_gateway.gateway.LLMGateway.generate", side_effect=mock_func):
        prompt = "Crie um projeto de analytics para analisar vendas baseado no dataset vendas.csv."
        dataset = "d_input/a_datasets/a_raw/vendas.csv"
        
        response = adapter.create_project(prompt, dataset_path=dataset, domain="analytics")
        
        # O Pipeline deve fluir inteiro sem interrupções
        assert response.success is True
        assert response.status == "READY"
        
        project_id = response.project_id
        
        # Verificar arquivos gerados no disco
        gen_path = os.path.join("e_generated_projects", "analytics", project_id)
        assert os.path.exists(gen_path)
        assert os.path.exists(os.path.join(gen_path, "main.py"))
        assert os.path.exists(os.path.join(gen_path, "test_main.py"))
        assert os.path.exists(os.path.join(gen_path, "CERTIFICATION.md"))
        
        # Limpeza para não poluir
        shutil.rmtree(gen_path, ignore_errors=True)

# pyrefly: ignore [missing-import]
import pytest
import os
import shutil
from unittest.mock import patch
from a_platform.b_interfaces.a_ide.adapter import IDEAdapter
from c_tests.end_to_end.mock_gateway import get_mocked_generate_function

def test_repair_loop_e2e():
    """
    Simula uma requisição onde o código gerado inicialmente tem um erro de sintaxe.
    O Validation Gate deve falhar, acionar o Repair Loop e o sistema deve ser curado e aprovado.
    """
    adapter = IDEAdapter()
    
    mock_func = get_mocked_generate_function(interactive=False, repair_error=True)
    
    with patch("a_platform.g_llm_gateway.gateway.LLMGateway.generate", side_effect=mock_func):
        prompt = "Crie um projeto de analytics sujeito a falha."
        dataset = "d_input/a_datasets/a_raw/vendas.csv"
        
        response = adapter.create_project(prompt, dataset_path=dataset, domain="analytics")
        
        # Como o repair_loop tem max_attempts=3, ele vai tentar 1 vez e o mock já devolve código consertado
        assert response.success is True
        assert response.status == "READY"
        
        project_id = response.project_id
        
        # Verificar arquivos gerados no disco e o selo de certificação
        gen_path = os.path.join("e_generated_projects", "analytics", project_id)
        assert os.path.exists(gen_path)
        assert os.path.exists(os.path.join(gen_path, "main.py"))
        
        # No main.py, esperamos que a versão corrigida (Success ETL) esteja no arquivo
        with open(os.path.join(gen_path, "main.py"), "r") as f:
            content = f.read()
            assert "Success ETL" in content
            
        cert_path = os.path.join(gen_path, "CERTIFICATION.md")
        assert os.path.exists(cert_path)
        
        with open(cert_path, "r") as f:
            cert_content = f.read()
            # Certificar que teve tentativa de reparo
            assert "- Repair Attempts: 1" in cert_content or "- Repair Attempts: 2" in cert_content
        
        # Limpeza
        shutil.rmtree(gen_path, ignore_errors=True)

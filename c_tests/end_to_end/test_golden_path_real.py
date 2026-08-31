# pyrefly: ignore [missing-import]
import os
import pytest
from a_platform.b_interfaces.a_ide.adapter import IDEAdapter

def test_golden_path_real_e2e():
    """
    Teste E2E de Caminho Dourado (Golden Path) utilizando o provedor LLM real.
    Valida a geração de código, materialização física, execução, validação, qualidade e certificação reais.
    
    Este teste requer uma chave de API válida.
    """
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("Chave de API não configurada para teste E2E real")
        
    adapter = IDEAdapter()
    
    prompt = "Crie um projeto analítico simples em Python que leia dados_vendas.csv, calcule KPIs e escreva testes unitários para as funções. NÃO gere tarefas de documentação ou infraestrutura. O domínio deste projeto é estritamente 'analytics'."
    
    dataset_dir = "d_input/a_datasets/a_raw"
    os.makedirs(dataset_dir, exist_ok=True)
    dataset_path = os.path.join(dataset_dir, "dados_vendas.csv")
    
    if not os.path.exists(dataset_path):
        with open(dataset_path, "w") as f:
            f.write("id_venda,valor,data\n1,100.50,2023-01-01\n2,200.00,2023-01-02\n")
            
    response = adapter.create_project(prompt=prompt, dataset_path=dataset_path, domain="analytics")
    
    if response.status == "NEEDS_INPUT":
        # Simula resposta do usuário e continua
        response = adapter.continue_project(response.project_id, "Use sqlite como banco de dados e prossiga sem mais dúvidas.")
        
    assert response.success is True, f"Pipeline falhou: {response.error}"
    assert response.status == "READY", f"O projeto não obteve status READY, status atual: {response.status}"
    
    project_id = response.project_id
    project_dir = os.path.join("e_generated_projects", "analytics", project_id)
    
    assert os.path.exists(project_dir), f"Diretório do projeto não encontrado: {project_dir}"
    
    # Validações estruturais avançadas de Analytics Layer E2E
    assert any(f.endswith('.py') for f in os.listdir(project_dir)), "Nenhum arquivo Python materializado no projeto (ETL falhou)."
    assert any(f.endswith('.sql') for f in os.listdir(project_dir)), "Nenhum arquivo SQL materializado no projeto (Banco/Analytics falhou)."
    assert any(f.startswith('test_') and f.endswith('.py') for f in os.listdir(project_dir)), "Nenhum arquivo de teste materializado no projeto (Testing falhou)."
    
    # Validações de infra
    assert os.path.exists(os.path.join(project_dir, "requirements.txt")) or os.path.exists(os.path.join(project_dir, "Dockerfile")), "Nenhum artefato de infraestrutura/requirements."
    assert os.path.exists(os.path.join(project_dir, "venv")), "Ambiente virtual (venv) não foi criado."

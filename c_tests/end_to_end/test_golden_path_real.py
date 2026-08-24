# pyrefly: ignore [missing-import]
import os
import pytest
from a_platform.a_interfaces.a_ide.adapter import IDEAdapter

def test_golden_path_real_e2e():
    """
    Teste E2E de Caminho Dourado (Golden Path) utilizando o provedor LLM real.
    Valida a geração de código, materialização física, execução, validação, qualidade e certificação reais.
    
    Este teste requer uma chave de API válida.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("Chave de API (OPENAI_API_KEY) não configurada para teste E2E real")
        
    adapter = IDEAdapter()
    
    prompt = "Crie um pipeline ETL simples em Python que leia dados_vendas.csv e calcule faturamento total."
    # dataset_path tem que existir, ou mockar o caminho? O prompt pede "dados_vendas.csv", vamos passar algo ou deixar que o LLM crie o dummy.
    # O user pediu dataset_path="d_input/a_datasets/a_raw/dados_vendas.csv". Para rodar localmente sem quebrar, vamos garantir que o dataset existe ou passar None.
    # Se passarmos o caminho, a plataforma pode tentar fazer profiling de arquivo inexistente.
    # Vou criar um CSV dummy antes de rodar para garantir que o Profiling funcione.
    
    dataset_dir = "d_input/a_datasets/a_raw"
    os.makedirs(dataset_dir, exist_ok=True)
    dataset_path = os.path.join(dataset_dir, "dados_vendas.csv")
    
    if not os.path.exists(dataset_path):
        with open(dataset_path, "w") as f:
            f.write("id_venda,valor,data\n1,100.50,2023-01-01\n2,200.00,2023-01-02\n")
            
    response = adapter.create_project(prompt=prompt, dataset_path=dataset_path, domain="analytics")
    
    assert response.success is True, f"Pipeline falhou: {response.error}"
    assert response.status == "READY", "O projeto não obteve status READY"
    
    project_id = response.project_id
    project_dir = os.path.join("e_generated_projects", "analytics", project_id)
    
    assert os.path.exists(project_dir), f"Diretório do projeto não encontrado: {project_dir}"
    assert os.path.exists(os.path.join(project_dir, "main.py")) or os.path.exists(os.path.join(project_dir, "app.py")) or any(f.endswith('.py') for f in os.listdir(project_dir)), "Nenhum arquivo Python materializado no projeto."
    
    # Validações estruturais básicas de materialização
    assert os.path.exists(os.path.join(project_dir, ".venv")), "Ambiente virtual (venv) não foi criado."

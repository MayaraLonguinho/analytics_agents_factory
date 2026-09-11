import os
import json
import logging
from pprint import pprint

from a_platform.c_brain.j_brain import Brain
from a_platform.a_core.b_domain.g_project_request import ProjectRequest
from a_platform.a_core.b_domain.f_project_plan import ProjectPlan, Task
from a_platform.c_brain.g_graph.b_graph_builder import GraphBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    print("="*50)
    print("🧠 AAF Brain - Operação de Demonstração")
    print("="*50)
    
    print("\n[1] Carregando o Brain e Registries...")
    brain = Brain()
    print("Brain carregado com sucesso. (Knowledge, Rules, Patterns, Domains, Agents, Skills, MCPs)")
    
    print("\n[2] Criando requisição de contexto simulada...")
    # Simulate a context request
    context_request = {
        "project_type": "Data Pipeline",
        "business_context": "Ingestão e transformação de vendas para dashboard executivo.",
        "domain": "data_engineering",
        "capabilities": ["etl_scripting", "dataset_profiling"],
        "dataset_profile": {
            "file_name": "vendas.csv",
            "schema": [{"col": "id", "type": "int"}, {"col": "valor", "type": "float"}],
            "row_count": 1000
        },
        "architecture": {
            "architecture_pattern": "Data Lakehouse"
        },
        "decisions": ["Usar duckdb para storage local", "Gerar scripts em python"]
    }
    
    print("\n[3] Gerando Context Pack compacto (Orçamento: 50.000 tokens)...")
    pack = brain.generate_context_pack(context_request)
    print("Context Pack gerado. Resumo:")
    print(f"  - Domínio: {pack['project'].get('domain')}")
    print(f"  - Arquitetura: {pack['architecture'].get('architecture_pattern')}")
    print(f"  - Rules de Arquitetura incluídas: {len(pack.get('architecture_rules', []))}")
    print(f"  - Platform Stack items: {len(pack.get('platform_stack', {}))}")
    
    print("\n[4] Preparando representação em Grafo (Project -> Context -> Dataset -> Decision -> Domain -> Capability -> Skill -> Agent -> MCP -> Gate)...")
    
    # Criar um ProjectRequest com um ProjectPlan para simular as tarefas
    req = ProjectRequest(
        prompt="Demo Prompt",
        project_id="demo-001",
        business_context=context_request["business_context"],
        domain=context_request["domain"],
        discovery_data={"requirement1": "Alta performance"},
        dataset_profile=context_request["dataset_profile"],
        architecture_decision=context_request["architecture"]
    )
    
    plan = ProjectPlan(project_id="demo-001", domain=context_request["domain"], materializer="a_materializer")
    task1 = Task(
        id="t1", 
        name="Ingestão de Dados", 
        description="Ingestão de Vendas",
        agent="DataAgent", 
        skills=["etl_scripting", "dataset_profiling"], 
        mcps=["filesystem_mcp", "database_mcp"], 
        expected_artifacts=["pipeline.py"]
    )
    plan.add_task(task1)
    req.project_plan = plan
    
    gb = GraphBuilder()
    graph_data = gb.build_graph(req)
    
    print("\n[5] Exportação de Grafos")
    print(f"Total de Nós gerados: {len(graph_data['nodes'])}")
    print(f"Total de Arestas geradas: {len(graph_data['edges'])}")
    print(f"Grafos salvos no diretório de runtime: {gb.base_dir}")
    print(" - Obsidian Vault pronto.")
    print(" - Graphify JSON gerado.")
    
    print("\n✨ Demonstração concluída com sucesso.")

if __name__ == "__main__":
    main()

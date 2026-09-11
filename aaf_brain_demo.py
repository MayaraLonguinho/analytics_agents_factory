import os
import json
import logging
from pprint import pprint

from a_platform.c_brain.j_brain import Brain
from a_platform.c_brain.j_brain import Brain
from a_platform.a_core.b_domain.i_execution_context import ExecutionContext
from a_platform.a_core.b_domain.f_project_plan import ProjectPlan, Task
from a_platform.c_brain.g_graph.b_graph_builder import GraphBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    print("="*50)
    print("🧠 AAF Brain - Operação de Demonstração")
    print("="*50)
    
    # Mocking OpenAI to avoid requiring pip install openai for demo
    from a_platform.g_llm_gateway.b_providers.d_openai.a_provider import OpenAIProvider
    from a_platform.g_llm_gateway.f_interfaces.a_base_provider import LLMResponse
    OpenAIProvider._initialize_client = lambda self: None
    async def mock_generate(self, request):
        return LLMResponse(content="", model=request.model, provider="openai")
    OpenAIProvider.generate = mock_generate
    
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
    
    print("\n[3] Simulando Discovery Interativo...")
    from a_platform.d_agents.b_discovery.a_discovery_agent import DiscoveryAgent, DiscoveryStatus
    from a_platform.g_llm_gateway.e_gateway import LLMGateway
    import asyncio
    
    gateway = LLMGateway()
    discovery = DiscoveryAgent(gateway=gateway, max_questions=5)
    
    # Criar um ExecutionContext real para a simulação
    req = ExecutionContext(
        prompt="Preciso de um pipeline de vendas que puxe dados em CSV e grave num BD, foque em alta performance.",
        project_id="demo-001",
        domain="data_engineering"
    )
    
    # Simulando um loop de interação com o usuário (perguntas sendo feitas até 5)
    async def simulate_discovery():
        for i in range(6): # Loop forzando a passar de 5
            status = await discovery.run_discovery(req, brain_instance=brain)
            if status == DiscoveryStatus.NEEDS_INPUT:
                question = req._discovery_data.get("missing_info_question")
                print(f"  -> Agent pergunta: {question}")
                # Simulando que o usuário responde "não sei"
                req._discovery_data["history"].append({"role": "user", "content": "não sei, decida você"})
            elif status == DiscoveryStatus.COMPLETE:
                print("  -> Discovery concluído e contexto congelado.")
                break
            elif status == DiscoveryStatus.FAILED:
                print("  -> (Mock) LLM falhou, forçando o atingimento do limite de 5 perguntas para o demo...")
                req._discovery_data["question_count"] = 5
                # Tenta novamente para que o código de "limite atingido" seja executado
                await discovery.run_discovery(req, brain_instance=brain)
                break
                
    asyncio.run(simulate_discovery())
    
    print("\n[4] Decisões Registradas:")
    for d in req.decisions:
        print(f"  [{d.id}] {d.status.upper()} - {d.decision} (Motivo: {d.reason})")
        
    print(f"Status do Gate Discovery: {req.gates.discovery}")
    
    print("\n[5] Gerando Context Pack compacto a partir do ExecutionContext...")
    # Preparar req dict for context pack
    context_request = {
        "project_type": req.project_type,
        "business_context": req.business_context,
        "domain": req.domain,
        "capabilities": ["etl_scripting"],
        "dataset_profile": {},
        "architecture": req.architecture_decision,
        "decisions": [{"id": d.id, "decision": d.decision} for d in req.decisions]
    }
    
    pack = brain.generate_context_pack(context_request)
    print("Context Pack gerado. Resumo:")
    print(f"  - Domínio: {pack['project'].get('domain')}")
    print(f"  - Arquitetura: {pack['architecture'].get('architecture_pattern')}")
    print(f"  - Regras Team Standard injetadas: {len(pack.get('team_standards', []))}")
    print(f"  - Platform Stack items: {len(pack.get('platform_stack', {}))}")
    
    print("\n[6] Preparando representação em Grafo...")
    
    # Adicionar o plano ao context
    plan = ProjectPlan(project_id="demo-001", domain=req.domain or "data_engineering", materializer="a_materializer")
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

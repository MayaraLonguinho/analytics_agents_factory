import sys
import argparse
import os
import uuid
import json

from a_platform.a_core.d_session.c_state import StateManager
from a_platform.a_core.d_session.b_context import ExecutionContext
from a_platform.n_orchestration.a_orchestrator import MasterOrchestrator

def cmd_start(args):
    print("=" * 50)
    print("🧠 Analytics Agents Factory (AAF) - CLI")
    print("=" * 50)
    
    prompt = input("\nDescreva o projeto que deseja construir:\n> ")
    if not prompt.strip():
        print("Erro: A descrição não pode ser vazia.")
        sys.exit(1)
        
    dataset = input("\n[Opcional] Caminho para o dataset (ou pressione Enter para pular):\n> ").strip()
    dataset = dataset if dataset else None
    
    project_id = str(uuid.uuid4())[:8]
    print(f"\n[AAF] Iniciando projeto... ID: {project_id}")
    
    # Execução real do orchestrator
    ctx = ExecutionContext(project_id=project_id, domain="analytics") # domínio base, depois é resolvido
    # Dummy discovery inject to avoid needs input loop if it's not interactive
    ctx.discovery_data = {"project_type": "CLI_REQUEST", "business_context": prompt, "domain": "analytics"}
    
    orchestrator = MasterOrchestrator()
    result = orchestrator.execute_pipeline(ctx)
    
    if result == "SUCCESS":
        print("\n✅ PROJETO CONCLUÍDO COM SUCESSO!")
        print(f"ID do Projeto: {project_id}")
        print("Você pode usar `aaf status <project_id>` ou `aaf result <project_id>` para ver os artefatos gerados.")
    elif result == "PAUSED":
        print("\n⏳ PROJETO PAUSADO PARA INPUT. Use interface para continuar.")
    else:
        print(f"\n❌ FALHA NA CONSTRUÇÃO DO PROJETO.")

def cmd_status(args):
    project_id = args.project_id
    try:
        sm, _ = StateManager.load_state(project_id)
        status = sm.get_status()
        print(f"Status do Projeto: {project_id}")
        print(f"Fase Atual: {status['current_phase']}")
        print(f"Pronto: {'Sim' if status['project_ready'] else 'Não'}")
    except FileNotFoundError:
        print(f"Erro: Projeto '{project_id}' não encontrado.")


def cmd_result(args):
    project_id = args.project_id
    try:
        sm, request = StateManager.load_state(project_id)
        if not sm.project_ready:
            print("O projeto ainda não está pronto.")
            return
            
        print("=" * 50)
        print(f"Resultado do Projeto: {project_id}")
        print("=" * 50)
        print(f"Domínio Final: {request.domain}")
        if request.architecture_decision:
            print("\nArquitetura Adotada:")
            print(f"- Padrão: {request.architecture_decision.get('architecture_pattern')}")
            
        if request.artifacts:
            print("\nArtefatos Gerados:")
            for art in request.artifacts:
                print(f" - [{art.type}] {art.name}")
        else:
            print("\nNenhum artefato encontrado no registro de sessão.")
            
    except FileNotFoundError:
        print(f"Erro: Projeto '{project_id}' não encontrado.")


def cmd_mcp(args):
    print("=" * 50)
    print("🛠️  AAF - MCP Executable Verification")
    print("=" * 50)
    
    from a_platform.f_mcp.e_executor.a_executor import MCPExecutor
    from a_platform.f_mcp.d_registry.a_registry import MCPRegistry
    
    executor = MCPExecutor()
    registry = MCPRegistry()
    
    mcps = registry.mcps
    if not mcps:
        print("Nenhum MCP registrado.")
        return

    for mcp_id, mcp_def in mcps.items():
        print(f"\n--- {mcp_def.name} ---")
        try:
            # Testes reais para cada MCP baseados em inputs válidos (somente listagem)
            if mcp_id == "filesystem_mcp":
                result = executor.execute("filesystem_mcp", operation="list", path=".")
            elif mcp_id == "database_mcp":
                result = executor.execute("database_mcp", operation="query", database=":memory:", query="SELECT 1 as check")
            elif mcp_id == "docker_mcp":
                result = executor.execute("docker_mcp", command="docker info")
            else:
                result = {"status": "UNKNOWN", "message": "Nenhum teste pré-definido para este MCP."}
                
            status = result.get("status")
            if status == "ok" or status == "SUCCESS":
                print(f"{mcp_id}: PASS")
            elif status == "NOT_AVAILABLE":
                print(f"{mcp_id}: NOT_AVAILABLE ({result.get('message', '')})")
            else:
                print(f"{mcp_id}: FAILED ({result.get('message', 'Erro desconhecido')})")
                
        except Exception as e:
            print(f"{mcp_id}: ERROR ({str(e)})")
            
    print("=" * 50)


def cmd_brain(args):
    print("=" * 50)
    print("🧠 AAF - Brain Verification")
    print("=" * 50)
    
    from a_platform.c_brain.h_brain import Brain
    brain = Brain()
    
    print("\n[Brain] Knowledge:")
    for k in brain.knowledge_registry._data.keys():
        print(f" - {k}")
        
    print("\n[Brain] Rules & Team Standards:")
    for k in brain.rule_registry._data.keys():
        print(f" - {k}")
        
    print("\n[Brain] Patterns:")
    for k in brain.pattern_registry._data.keys():
        print(f" - {k}")
        
    print("\n[Brain] Domains:")
    for k in brain.domain_registry.domains.keys():
        print(f" - {k}")
        
    print("\n[Brain] Skills:")
    for k in brain.skill_registry.skills.keys():
        print(f" - {k}")
        
    print("\n[Brain] Agents:")
    for k in brain.agent_registry.agents.keys():
        print(f" - {k}")
    
    print("\nConhecimento estático carregado com sucesso!")
    print("=" * 50)

def main():
    parser = argparse.ArgumentParser(description="Analytics Agents Factory CLI")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")
    
    # aaf start
    subparsers.add_parser("start", help="Inicia uma nova sessão da fábrica")
    
    # aaf status <project_id>
    parser_status = subparsers.add_parser("status", help="Checa o status de um projeto")
    parser_status.add_argument("project_id", help="ID do projeto")
    
    # aaf result <project_id>
    parser_result = subparsers.add_parser("result", help="Mostra o resultado de um projeto finalizado")
    parser_result.add_argument("project_id", help="ID do projeto")
    
    # aaf mcp
    subparsers.add_parser("mcp", help="Verificações reais dos MCPs")
    
    # aaf brain
    subparsers.add_parser("brain", help="Acessar conteúdo do Brain real")
    
    args = parser.parse_args()
    
    if args.command == "start":
        cmd_start(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "result":
        cmd_result(args)
    elif args.command == "mcp":
        cmd_mcp(args)
    elif args.command == "brain":
        cmd_brain(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

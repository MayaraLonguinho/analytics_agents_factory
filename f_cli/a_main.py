import argparse
import sys
import json
import logging
import uuid

from a_platform.b_contracts.z_interfaces.a_ide_adapter import IDEAdapter
from a_platform.b_contracts.j_state_manager import StateManager
from a_platform.c_brain import Brain
from a_platform.f_mcps.d_registry.a_registry import MCPRegistry
from g_configuration.a_settings import settings

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("aaf_cli")

def handle_start(args):
    logger.info("Iniciando Analytics Agents Factory (AAF)...")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    
    adapter = IDEAdapter()
    project_id = args.project_id
    
    # Caso 1: Verificar se é uma retomada de sessão existente
    if project_id and StateManager.state_exists(project_id):
        sm, req = StateManager.load_state(project_id)
        if sm.current_phase.name == "NEEDS_INPUT":
            logger.info(f"[AAF] Sessão existente '{project_id}' pausada aguardando resposta.")
            answer = args.answer or args.prompt
            
            if not answer and sys.stdin.isatty():
                pending_q = sm.get_pending_question(req) or "Mais informações são necessárias para o projeto."
                logger.info(f"\n[AAF Discovery] Pergunta Pendente:\n{pending_q}")
                try:
                    answer = input("\nSua resposta: ").strip()
                except (EOFError, KeyboardInterrupt):
                    logger.info("\nOperação cancelada pelo usuário.")
                    sys.exit(0)
            
            if not answer:
                pending_q = sm.get_pending_question(req) or "Mais informações necessárias."
                logger.info(f"\n[AAF Discovery] Pergunta Pendente:\n{pending_q}")
                logger.info(f"Para responder, execute: aaf start --project-id {project_id} --answer \"<sua resposta>\"")
                sys.exit(0)
                
            logger.info(f"[AAF] Retomando Discovery com resposta do usuário...")
            res = adapter.continue_project(project_id, answer)
            _handle_adapter_result(res)
            return
            
        elif sm.project_ready:
            logger.info(f"[AAF] O projeto '{project_id}' já está concluído (PROJECT READY = YES).")
            return

    # Caso 2: Novo projeto
    prompt = args.prompt
    if not prompt and sys.stdin.isatty():
        try:
            prompt = input("Descreva o projeto de analytics que deseja construir: ").strip()
        except (EOFError, KeyboardInterrupt):
            logger.info("\nOperação cancelada pelo usuário.")
            sys.exit(0)
            
    if not prompt:
        logger.error("Erro: O argumento --prompt é obrigatório para iniciar um novo projeto.")
        sys.exit(1)
        
    if not project_id:
        project_id = f"prj_{uuid.uuid4().hex[:8]}"
        
    res = adapter.create_project(prompt=prompt, dataset_path=args.dataset, project_id=project_id)
    _handle_adapter_result(res)

def _handle_adapter_result(res: dict):
    status = res.get("status")
    proj_id = res.get("project_id")
    
    if status == "NEEDS_INPUT":
        logger.info(f"\n=======================================================")
        logger.info(f"[AAF Discovery] PAUSED - Aguardando Resposta do Usuário")
        logger.info(f"Projeto ID: {proj_id}")
        logger.info(f"Pergunta:\n{res.get('question')}")
        logger.info(f"=======================================================")
        logger.info(f"Para responder, execute: aaf start --project-id {proj_id} --answer \"<sua resposta>\"")
        sys.exit(0)
    elif status == "SUCCESS":
        logger.info(f"\n=======================================================")
        logger.info(f"🏆 PROJECT READY = YES ({proj_id})")
        logger.info(f"=======================================================")
        sys.exit(0)
    else:
        logger.error(f"\n=======================================================")
        logger.error(f"❌ PROJECT READY = NO ({proj_id})")
        logger.error(f"Detalhes: {res.get('question', 'Erro desconhecido')}")
        logger.error(f"=======================================================")
        sys.exit(1)

def handle_status(args):
    try:
        sm, _ = StateManager.load_state(args.project_id)
        status_data = sm.get_status()
        logger.info(json.dumps(status_data, indent=2))
    except FileNotFoundError:
        logger.error(f"Nenhum estado encontrado para o projeto {args.project_id}")

def handle_result(args):
    try:
        _, request = StateManager.load_state(args.project_id)
        logger.info(f"Project Ready: {request.metadata.get('PROJECT_READY', 'UNKNOWN')}")
        logger.info(f"Generated Path: {getattr(request.project_context, 'project_path', 'N/A')}")
    except FileNotFoundError:
        logger.error(f"Nenhum resultado encontrado para o projeto {args.project_id}")

def handle_brain(args):
    brain = Brain()
    logger.info("--- AAF Brain Operacional ---")
    logger.info(f"Rules Roles: {len(brain.get_rules('role'))}")
    logger.info(f"Team Standards: {len(brain.get_rules('team_standard'))}")
    logger.info("O Brain está ativo e os domínios estão registrados.")

def handle_mcp(args):
    registry = MCPRegistry()
    mcps = registry.list_mcps()
    logger.info("--- MCP Registry ---")
    for mcp in mcps:
        logger.info(f"- {mcp.id} (v{mcp.version}): {mcp.description}")
        logger.info(f"  Capabilities: {mcp.capabilities}\n")

def main():
    parser = argparse.ArgumentParser(description="Analytics Agents Factory CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Start
    start_parser = subparsers.add_parser("start", help="Inicia ou retoma o fluxo do AAF")
    start_parser.add_argument("--project-id", help="ID Único do projeto", default=None)
    start_parser.add_argument("--prompt", help="Descrição do que construir ou resposta de continuação", default=None)
    start_parser.add_argument("--dataset", help="Caminho para o dataset de análise", default=None)
    start_parser.add_argument("--answer", help="Resposta direta a pergunta pendente de Discovery", default=None)
    
    # Status
    status_parser = subparsers.add_parser("status", help="Verifica o estado atual")
    status_parser.add_argument("project_id", help="ID do projeto")
    
    # Result
    result_parser = subparsers.add_parser("result", help="Verifica o resultado da geração")
    result_parser.add_argument("project_id", help="ID do projeto")
    
    # Brain
    subparsers.add_parser("brain", help="Expõe as políticas e domínios do Brain")
    
    # MCP
    subparsers.add_parser("mcp", help="Lista as abstrações MCP disponíveis")
    
    args = parser.parse_args()
    
    if args.command == "start": handle_start(args)
    elif args.command == "status": handle_status(args)
    elif args.command == "result": handle_result(args)
    elif args.command == "brain": handle_brain(args)
    elif args.command == "mcp": handle_mcp(args)

if __name__ == "__main__":
    main()

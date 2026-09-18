import argparse
import sys
import json
import logging
from a_platform.n_orchestration.a_orchestrator import MasterOrchestrator
from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts.f_state_manager import StateManager
from a_platform.c_brain import Brain
from a_platform.f_mcps.d_registry.a_registry import MCPRegistry
from g_configuration.a_settings import settings

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("aaf_cli")

def handle_start(args):
    logger.info("Iniciando Analytics Agents Factory (AAF)...")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    
    request = ExecutionContext(
        project_id=args.project_id,
        prompt=args.prompt,
        dataset_path=args.dataset
    )
    
    try:
        orchestrator = MasterOrchestrator()
        result = orchestrator.execute_pipeline(request)
        logger.info(f"Pipeline Result: {result}")
    except Exception as e:
        logger.error("PROJECT READY = NO")
        logger.error(f"Etapa: Initialization/Pipeline")
        logger.error(f"Evidencia: Exception")
        logger.error(f"Erro: {str(e)}")
        logger.error(f"Causa: Configuração ausente ou falha de execução.")
        sys.exit(1)



def handle_status(args):
    try:
        sm, _ = StateManager.load_state(args.project_id)
        status_data = sm.get_status()
        logger.info(json.dumps(status_data, indent=2))
    except FileNotFoundError:
        logger.error(f"Nenhum estado encontrado para o projeto {args.project_id}")

def handle_result(args):
    # O result no AAF reside no path final da materialização e nos relatorios salvos.
    # Por hora extraímos do state.
    try:
        _, request = StateManager.load_state(args.project_id)
        logger.info(f"Project Ready: {request.metadata.get("PROJECT_READY", "UNKNOWN")}")
        logger.info(f"Generated Path: {getattr(request.project_context, "project_path", "N/A")}")
    except FileNotFoundError:
        logger.error(f"Nenhum resultado encontrado para o projeto {args.project_id}")

def handle_brain(args):
    brain = Brain()
    logger.info("--- AAF Brain Opeacional ---")
    logger.info(f"Rules Roles: {len(brain.get_rules("role"))}")
    logger.info(f"Team Standards: {len(brain.get_rules("team_standard"))}")
    # Simula um dump rapido
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
    start_parser = subparsers.add_parser("start", help="Inicia o fluxo do AAF")
    start_parser.add_argument("--project-id", required=True, help="ID Único do projeto")
    start_parser.add_argument("--prompt", required=True, help="Descrição do que construir")
    start_parser.add_argument("--dataset", help="Caminho para o dataset de análise", default=None)
    
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

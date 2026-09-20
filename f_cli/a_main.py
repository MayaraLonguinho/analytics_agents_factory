"""
f_cli/a_main.py
===============
Interface de linha de comando (CLI) do Analytics Agents Factory (AAF).
Responsabilidade estrita: INPUT + TRANSPORT + PRESENTATION.

Não implementa orquestração, regras de negócio, planejamento, atribuição
de agentes, roteamento de skills, diagnóstico de causa raiz ou cálculo de prontidão.
"""
import argparse
import json
import logging
import sys
import uuid
from pathlib import Path

# Garante que a raiz do repositório esteja no sys.path ao invocar o script diretamente
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from a_platform.b_contracts.z_interfaces.a_ide_adapter import IDEAdapter
from a_platform.b_contracts.j_state_manager import StateManager
from a_platform.c_brain import Brain
from a_platform.f_mcps.d_registry.a_registry import MCPRegistry
from g_configuration.a_settings import settings

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("aaf_cli")


def handle_start(args: argparse.Namespace) -> None:
    """
    Submete uma nova solicitação de fabricação de projeto para o AAF.
    """
    logger.info("Iniciando Analytics Agents Factory (AAF)...")
    logger.info(f"LLM Provider: {settings.llm_provider}")

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

    project_id = args.project_id
    if not project_id:
        project_id = f"prj_{uuid.uuid4().hex[:8]}"

    adapter = IDEAdapter()
    res = adapter.create_project(prompt=prompt, dataset_path=args.dataset, project_id=project_id)
    _handle_adapter_result(res)


def handle_resume(args: argparse.Namespace) -> None:
    """
    Retoma a execução de um projeto existente pausado (NEEDS_INPUT).
    Encaminha a resposta do usuário para a interface da plataforma sem assumir
    fase responsável ou implementar lógica de orquestração localmente.
    """
    project_id = getattr(args, "project_id", None) or getattr(args, "project_id_flag", None)
    if not project_id:
        logger.error("Erro: O ID do projeto é obrigatório para retomar a execução.")
        sys.exit(1)

    answer = getattr(args, "answer", None)
    if not answer and sys.stdin.isatty():
        if StateManager.state_exists(project_id):
            try:
                sm, req = StateManager.load_state(project_id)
                pending_q = sm.get_pending_question(req)
                if pending_q:
                    logger.info(f"\n[AAF] Pergunta pendente ({project_id}):\n{pending_q}")
            except Exception:
                pass
        try:
            answer = input("\nSua resposta: ").strip()
        except (EOFError, KeyboardInterrupt):
            logger.info("\nOperação cancelada pelo usuário.")
            sys.exit(0)

    if not answer:
        logger.error("Erro: O argumento --answer é obrigatório para retomar o projeto.")
        logger.info(f"Para responder, execute: python f_cli/a_main.py resume {project_id} --answer \"<sua resposta>\"")
        sys.exit(1)

    logger.info(f"[AAF] Retomando projeto '{project_id}'...")
    adapter = IDEAdapter()
    res = adapter.continue_project(project_id, answer)
    _handle_adapter_result(res)


def _handle_adapter_result(res: dict) -> None:
    """
    Apresenta de forma genérica o resultado retornado pela interface da plataforma.
    Não infere Readiness por conta própria nem associa NEEDS_INPUT exclusivamente ao Discovery.
    """
    status = res.get("status")
    proj_id = res.get("project_id")

    if status == "NEEDS_INPUT":
        logger.info("\n=======================================================")
        logger.info("[AAF] PAUSED - Aguardando resposta do usuário")
        logger.info(f"Projeto ID: {proj_id}")
        question = res.get("question") or "Mais informações são necessárias para prosseguir."
        logger.info(f"Pergunta / Instrução:\n{question}")
        logger.info("=======================================================")
        logger.info(f"Para responder, execute: python f_cli/a_main.py resume {proj_id} --answer \"<sua resposta>\"")
        sys.exit(0)
    elif status == "SUCCESS":
        logger.info("\n=======================================================")
        logger.info(f"🏆 PROJECT READY = YES ({proj_id})")
        logger.info("=======================================================")
        sys.exit(0)
    else:
        details = res.get("question") or res.get("details") or "Erro ou estado operacional não especificado"
        logger.error("\n=======================================================")
        logger.error(f"❌ Status: {status} ({proj_id})")
        logger.error(f"Detalhes: {details}")
        logger.error("=======================================================")
        sys.exit(1)


def handle_status(args: argparse.Namespace) -> None:
    """
    Consulta e apresenta o estado atual do projeto registrado no StateManager.
    """
    try:
        sm, _ = StateManager.load_state(args.project_id)
        status_data = sm.get_status()
        logger.info(json.dumps(status_data, indent=2))
    except FileNotFoundError:
        logger.error(f"Nenhum estado encontrado para o projeto {args.project_id}")
    except Exception as e:
        logger.error(f"Erro ao consultar estado do projeto {args.project_id}: {e}")


def handle_result(args: argparse.Namespace) -> None:
    """
    Apresenta o resultado da fabricação do projeto a partir dos metadados persistidos.
    """
    try:
        _, request = StateManager.load_state(args.project_id)
        logger.info(f"Project Ready: {request.metadata.get('PROJECT_READY', 'UNKNOWN')}")
        logger.info(f"Generated Path: {getattr(request.project_context, 'project_path', 'N/A')}")
    except FileNotFoundError:
        logger.error(f"Nenhum resultado encontrado para o projeto {args.project_id}")
    except Exception as e:
        logger.error(f"Erro ao consultar resultado do projeto {args.project_id}: {e}")


def handle_brain(args: argparse.Namespace) -> None:
    """
    Apresenta as regras e padrões registrados no Brain.
    """
    try:
        brain = Brain()
        logger.info("--- AAF Brain Operacional ---")
        logger.info(f"Rules Roles: {len(brain.get_rules('role'))}")
        logger.info(f"Team Standards: {len(brain.get_rules('team_standard'))}")
        logger.info("O Brain está ativo e os domínios estão registrados.")
    except Exception as e:
        logger.error(f"Erro ao consultar o Brain: {e}")


def handle_mcp(args: argparse.Namespace) -> None:
    """
    Lista os servidores e capacidades registradas no MCP Registry.
    """
    try:
        registry = MCPRegistry()
        mcps = registry.list_mcps()
        logger.info("--- MCP Registry ---")
        for mcp in mcps:
            logger.info(f"- {mcp.id} (v{mcp.version}): {mcp.description}")
            logger.info(f"  Capabilities: {mcp.capabilities}\n")
    except Exception as e:
        logger.error(f"Erro ao consultar o MCP Registry: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analytics Agents Factory CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # start
    start_parser = subparsers.add_parser("start", help="Inicia uma nova solicitação no AAF")
    start_parser.add_argument("--project-id", help="ID único do projeto (opcional, gerado automaticamente se omitido)", default=None)
    start_parser.add_argument("--prompt", help="Descrição do que construir no projeto", default=None)
    start_parser.add_argument("--dataset", help="Caminho para o dataset de análise (opcional)", default=None)

    # resume
    resume_parser = subparsers.add_parser("resume", help="Retoma a execução de um projeto pausado (NEEDS_INPUT)")
    resume_parser.add_argument("project_id", nargs="?", default=None, help="ID do projeto a ser retomado")
    resume_parser.add_argument("--project-id", dest="project_id_flag", default=None, help="ID do projeto (alternativa ao argumento posicional)")
    resume_parser.add_argument("--answer", help="Resposta às perguntas ou instruções do AAF", default=None)

    # status
    status_parser = subparsers.add_parser("status", help="Consulta o estado atual da máquina de estados do projeto")
    status_parser.add_argument("project_id", help="ID do projeto")

    # result
    result_parser = subparsers.add_parser("result", help="Consulta o resultado e o path do projeto gerado")
    result_parser.add_argument("project_id", help="ID do projeto")

    # brain
    subparsers.add_parser("brain", help="Apresenta as regras e domínios operacionais do Brain")

    # mcp
    subparsers.add_parser("mcp", help="Lista as abstrações e capacidades disponíveis no MCP Registry")

    args = parser.parse_args()

    if args.command == "start":
        handle_start(args)
    elif args.command == "resume":
        handle_resume(args)
    elif args.command == "status":
        handle_status(args)
    elif args.command == "result":
        handle_result(args)
    elif args.command == "brain":
        handle_brain(args)
    elif args.command == "mcp":
        handle_mcp(args)


if __name__ == "__main__":
    main()

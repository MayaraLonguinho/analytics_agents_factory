import argparse
import sys
import logging
from pprint import pprint

from a_platform.b_interfaces.a_ide.adapter import IDEAdapter

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Analytics Agents Factory CLI via IDE Adapter")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")
    
    # Comandos de inicialização (start/run/create)
    create_parser = subparsers.add_parser("create", help="Cria um novo projeto (Alias para start/run).")
    create_parser.add_argument("prompt", type=str, help="O prompt descrevendo o que deve ser criado.")
    create_parser.add_argument("--dataset", type=str, default=None, help="Caminho para a base de dados (opcional).")
    create_parser.add_argument("--domain", type=str, default=None, help="Domínio do projeto (opcional).")

    start_parser = subparsers.add_parser("start", help="Inicia um novo projeto. O IDE Agent DEVE usar este comando ou o adapter, e NÃO gerar código manualmente.")
    start_parser.add_argument("prompt", type=str, help="O prompt descrevendo o que deve ser criado.")
    start_parser.add_argument("--dataset", type=str, default=None, help="Caminho para a base de dados (opcional).")
    start_parser.add_argument("--domain", type=str, default=None, help="Domínio do projeto (opcional).")

    run_parser = subparsers.add_parser("run", help="Inicia um novo projeto (Alias para start).")
    run_parser.add_argument("prompt", type=str, help="O prompt descrevendo o que deve ser criado.")
    run_parser.add_argument("--dataset", type=str, default=None, help="Caminho para a base de dados (opcional).")
    run_parser.add_argument("--domain", type=str, default=None, help="Domínio do projeto (opcional).")
    
    # Comando 'continue'
    continue_parser = subparsers.add_parser("continue", help="Continua um projeto pausado (Discovery).")
    continue_parser.add_argument("project_id", type=str, help="ID do projeto em andamento.")
    continue_parser.add_argument("response", type=str, help="A resposta do usuário à pergunta da IDE.")
    
    # Comando 'status'
    status_parser = subparsers.add_parser("status", help="Verifica o status do projeto.")
    status_parser.add_argument("project_id", type=str, help="ID do projeto.")

    # Comando 'result'
    result_parser = subparsers.add_parser("result", help="Retorna o path do projeto se estiver pronto.")
    result_parser.add_argument("project_id", type=str, help="ID do projeto.")

    # Comando 'cancel'
    cancel_parser = subparsers.add_parser("cancel", help="Cancela o projeto abortando o progresso.")
    cancel_parser.add_argument("project_id", type=str, help="ID do projeto.")
    
    args = parser.parse_args()
    adapter = IDEAdapter()
    
    print("="*50)
    print("🚀 ANALYTICS AI FACTORY CORE")
    print("="*50)
    
    if args.command in ["create", "start", "run"]:
        res = adapter.create_project(args.prompt, args.dataset, args.domain)
        _print_res(res)
    elif args.command == "continue":
        res = adapter.continue_project(args.project_id, args.response)
        _print_res(res)
    elif args.command == "status":
        res = adapter.get_project_status(args.project_id)
        _print_res(res)
    elif args.command == "result":
        res = adapter.get_project_result(args.project_id)
        _print_res(res)
    elif args.command == "cancel":
        res = adapter.cancel_project(args.project_id)
        _print_res(res)
    else:
        parser.print_help()

def _print_res(res):
    print(f"Status: {res.status}")
    if res.message:
        print(f"Message: {res.message}")
    if res.error:
        print(f"Error: {res.error}")
        
    print("="*50)
    if res.status == "NEEDS_INPUT":
        print(f"O projeto {res.project_id} está pausado aguardando sua resposta.")
        print("Use o comando 'continue' passando o ID e a resposta.")
    elif res.status == "READY":
        print("✅ PIPELINE CONCLUÍDO COM SUCESSO. PROJECT READY = YES.")
    elif res.status == "FAILED":
        print("❌ FALHA NO PIPELINE. PROJECT READY = NO.")
        sys.exit(1)
        
if __name__ == "__main__":
    main()

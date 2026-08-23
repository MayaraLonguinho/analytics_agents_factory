import argparse
import logging
import uuid
import sys

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.c_orchestration.orchestrator import MasterOrchestrator

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def parse_args():
    parser = argparse.ArgumentParser(description="Analytics Agents Factory CLI")
    parser.add_argument("--prompt", type=str, required=True, help="O prompt descrevendo o que deve ser criado.")
    parser.add_argument("--dataset", type=str, default=None, help="Caminho para a base de dados (opcional).")
    parser.add_argument("--domain", type=str, default=None, help="Domínio do projeto (ex: analytics, ecommerce).")
    return parser.parse_args()

def main():
    args = parse_args()
    
    project_id = f"proj_{uuid.uuid4().hex[:8]}"
    request = ProjectRequest(
        prompt=args.prompt,
        dataset_path=args.dataset,
        domain=args.domain,
        project_id=project_id
    )
    
    print("="*50)
    print("🚀 ANALYTICS AI FACTORY - INICIANDO PIPELINE")
    print(f"Projeto: {project_id}")
    print(f"Prompt: {request.prompt}")
    print("="*50)
    
    orchestrator = MasterOrchestrator()
    success = orchestrator.execute_pipeline(request)
    
    print("="*50)
    if success:
        print("✅ PIPELINE CONCLUÍDO COM SUCESSO. PROJECT READY = YES.")
    else:
        print("❌ FALHA NO PIPELINE. PROJECT READY = NO.")
        print(orchestrator.state_manager.get_status())
        sys.exit(1)
    print("="*50)

if __name__ == "__main__":
    main()

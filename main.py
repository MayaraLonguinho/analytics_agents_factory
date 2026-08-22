import sys
from a_platform.a_core.c_orchestration.orchestrator import MasterOrchestrator

if __name__ == "__main__":
    prompt = "Crie um script simples de python que printe hello world e rode testes no pytest"
    if len(sys.argv) > 2:
        prompt = sys.argv[2]
        
    orchestrator = MasterOrchestrator()
    orchestrator.run_pipeline(prompt)

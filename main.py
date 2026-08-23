import sys
from a_platform.a_core.c_orchestration.orchestrator import MasterOrchestrator

if __name__ == "__main__":
    prompt = input("\\n[AAF] Qual projeto você deseja criar hoje?\\n-> ")
    
    orchestrator = MasterOrchestrator()
    orchestrator.run_pipeline(prompt)

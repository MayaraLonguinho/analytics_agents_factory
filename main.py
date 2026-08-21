import asyncio
import argparse
import sys
from a_platform.a_core.c_orchestration.orchestrator import MasterOrchestrator

# Simple ANSI colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

async def main():
    parser = argparse.ArgumentParser(description="Analytics AI Factory CLI")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run the E2E pipeline")
    run_parser.add_argument("prompt", type=str, help="Project prompt/intent")
    
    status_parser = subparsers.add_parser("status", help="Check system status")
    
    args = parser.parse_args()

    if args.command == "run":
        print(f"{CYAN}[AAF] Starting End-to-End Pipeline...{RESET}")
        print(f"{YELLOW}[INPUT]{RESET} {args.prompt}\n")
        
        orchestrator = MasterOrchestrator()
        state = await orchestrator.run_pipeline(args.prompt)
        
        final_status = state.get("status")
        if "COMPLETED_SUCCESS" in final_status:
            print(f"\n{GREEN}[SUCCESS] Pipeline Completed Successfully!{RESET}")
            cert = state.get("certification")
            print(f"Project ID: {cert.project_id} | Tier: {cert.tier} | Score: {cert.metrics.get('final_score')}")
        else:
            print(f"\n{RED}[FAILED] Pipeline ended with status: {final_status}{RESET}")
            
    elif args.command == "status":
        print(f"{CYAN}[AAF] Engine is ready.{RESET}")
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())

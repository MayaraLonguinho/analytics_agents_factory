import asyncio
import argparse
import sys
import os
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

    run_parser = subparsers.add_parser("run", help="Run the E2E pipeline via CLI")
    run_parser.add_argument("prompt", type=str, help="Project prompt/intent")
    
    status_parser = subparsers.add_parser("status", help="Check system status")
    
    serve_api_parser = subparsers.add_parser("serve-api", help="Start FastAPI REST Server")
    serve_ui_parser = subparsers.add_parser("serve-ui", help="Start Streamlit Web UI")
    
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
        
    elif args.command == "serve-api":
        print(f"{CYAN}[AAF] Starting API Server on port 8000...{RESET}")
        os.system("uvicorn a_platform.l_interfaces.api.main_api:app --host 0.0.0.0 --port 8000 --reload")
        
    elif args.command == "serve-ui":
        print(f"{CYAN}[AAF] Starting Web UI on port 8501...{RESET}")
        os.system("streamlit run a_platform/l_interfaces/ui/app.py")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["serve-api", "serve-ui"]:
        # Do not wrap os.system loops in asyncio.run as uvicorn/streamlit handle their own loops
        asyncio.run(main())
    else:
        asyncio.run(main())

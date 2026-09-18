import argparse

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analytics Agents Factory CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # aaf start
    start_parser = subparsers.add_parser("start", help="Start a new AAF project generation")
    start_parser.add_argument("--prompt", type=str, required=True, help="Project description")
    start_parser.add_argument("--dataset", type=str, help="Path to input dataset (optional)")

    # aaf status
    status_parser = subparsers.add_parser("status", help="Check status of a running project")
    status_parser.add_argument("--id", type=str, required=True, help="Project ID")

    # aaf result
    result_parser = subparsers.add_parser("result", help="Get generation results")
    result_parser.add_argument("--id", type=str, required=True, help="Project ID")

    # aaf brain
    subparsers.add_parser("brain", help="Access Brain knowledge and state")

    # aaf mcp
    mcp_parser = subparsers.add_parser("mcp", help="Execute MCP tools directly")
    mcp_parser.add_argument("--tool", type=str, required=True, help="Tool to run")

    return parser

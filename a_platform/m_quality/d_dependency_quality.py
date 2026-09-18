"""
DependencyQuality gate.

Evaluates whether 'pip check' was executed and returned exit code 0.
Uses CommandExecutionResult.executable and command argv for identification,
NOT substring search in stdout/stderr.
"""
from typing import List
from a_platform.b_contracts import CommandExecutionResult


def _is_pip_check(cr: CommandExecutionResult) -> bool:
    """True when the command is exactly 'pip check' (argv[0]=pip, argv[1]=check)."""
    return cr.executable == "pip" and len(cr.command) >= 2 and cr.command[1] == "check"


class DependencyQuality:
    def evaluate(self, cmd_results: List[CommandExecutionResult]) -> str:
        relevant = [c for c in cmd_results if _is_pip_check(c)]
        if not relevant:
            return "NOT_EXECUTED"
        if all(c.status == "SUCCESS" and c.return_code == 0 for c in relevant):
            return "PASSED"
        return "FAILED"

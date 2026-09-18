"""
SecurityQuality gate.

Evaluates whether bandit was executed and returned exit code 0.
Identification is based on CommandExecutionResult.executable.
"""
from typing import List
from a_platform.b_contracts import CommandExecutionResult

SECURITY_TOOLS = {"bandit"}


class SecurityQuality:
    def evaluate(self, cmd_results: List[CommandExecutionResult]) -> str:
        relevant = [c for c in cmd_results if c.executable in SECURITY_TOOLS]
        if not relevant:
            return "NOT_EXECUTED"
        if all(c.status == "SUCCESS" and c.return_code == 0 for c in relevant):
            return "PASSED"
        return "FAILED"

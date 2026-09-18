"""
CodeQuality gate.

Evaluates whether a code quality tool (ruff / flake8) was executed
and returned exit code 0. Identification is based on CommandExecutionResult.executable,
NOT on text search in stdout/stderr.
"""
from typing import List
from a_platform.b_contracts import CommandExecutionResult

# Recognised code-quality executables in the allowed command set
CODE_QUALITY_TOOLS = {"ruff", "flake8"}


class CodeQuality:
    def evaluate(self, cmd_results: List[CommandExecutionResult]) -> str:
        """
        Returns: "PASSED" | "FAILED" | "NOT_EXECUTED"
        NOT_EXECUTED is treated as FAILED by QualityEngine.
        """
        relevant = [c for c in cmd_results if c.executable in CODE_QUALITY_TOOLS]
        if not relevant:
            return "NOT_EXECUTED"
        # Any non-zero return code or DENIED/TIMEOUT = FAILED
        if all(c.status == "SUCCESS" and c.return_code == 0 for c in relevant):
            return "PASSED"
        return "FAILED"

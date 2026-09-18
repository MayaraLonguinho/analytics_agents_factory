"""
ExecutionValidation gate.

Rules:
  1. ExecutionResult must exist.
  2. status must be "PASSED".
  3. return_code must be 0 (or None when no commands ran — e.g. plan had no commands).
  4. No command in the commands list may have status DENIED or TIMEOUT.

stdout / stderr emptiness is NOT a failure criterion — a silent successful process is valid.
"""
from a_platform.b_contracts import ExecutionResult


class ExecutionValidation:
    def validate(self, runtime_result: ExecutionResult) -> bool:
        if runtime_result is None:
            return False

        if runtime_result.status != "PASSED":
            return False

        # return_code=None is acceptable when no commands ran (empty plan).
        if runtime_result.return_code is not None and runtime_result.return_code != 0:
            return False

        # Any denied or timed-out command is an execution failure
        blocking_statuses = {"DENIED", "TIMEOUT"}
        for cr in runtime_result.commands:
            if cr.status in blocking_statuses:
                return False

        return True

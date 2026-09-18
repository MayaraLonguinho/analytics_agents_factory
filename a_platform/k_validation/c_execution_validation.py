from a_platform.b_contracts import ExecutionResult

class ExecutionValidation:
    def validate(self, runtime_result: ExecutionResult) -> bool:
        if not runtime_result or runtime_result.status != "PASSED":
            return False
        if runtime_result.return_code != 0:
            return False
        if not runtime_result.evidence:
            return False
        # Absence of evidence = Failure
        if not runtime_result.stdout and not runtime_result.stderr:
            return False
        return True

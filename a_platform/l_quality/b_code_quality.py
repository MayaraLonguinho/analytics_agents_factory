class CodeQuality:
    def evaluate(self, runtime_result_dict: dict) -> str:
        if not runtime_result_dict:
            return "FAILED"
            
        stdout = runtime_result_dict.get("stdout", "").lower()
        stderr = runtime_result_dict.get("stderr", "").lower()
        commands = runtime_result_dict.get("command", [])
        
        # Check if code quality tools were actually executed
        executed = any(cmd for cmd in commands if "flake8" in cmd or "pylint" in cmd or "black" in cmd or "isort" in cmd)
        
        if not executed:
            return "NOT_EXECUTED"
            
        if "failed" in stdout or "failed" in stderr or "error" in stdout or "error" in stderr:
            return "FAILED"
        return "PASSED"

class SecurityQuality:
    def evaluate(self, runtime_result_dict: dict) -> str:
        if not runtime_result_dict:
            return "FAILED"
            
        stdout = runtime_result_dict.get("stdout", "").lower()
        stderr = runtime_result_dict.get("stderr", "").lower()
        commands = runtime_result_dict.get("command", [])
        
        executed = any(cmd for cmd in commands if "bandit" in cmd or "safety" in cmd)
        
        if not executed:
            return "NOT_EXECUTED"
            
        if "issue" in stdout or "vulnerability" in stdout or "failed" in stderr:
            return "FAILED"
        return "PASSED"

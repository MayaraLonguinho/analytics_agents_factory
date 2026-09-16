class CodeQuality:
    def evaluate(self, runtime_result_dict: dict) -> bool:
        if not runtime_result_dict:
            return False
            
        stdout = runtime_result_dict.get("stdout", "").lower()
        stderr = runtime_result_dict.get("stderr", "").lower()
        
        # ABSENCE OF EVIDENCE = FAILURE. Se o linter (flake8/pylint) ou testes (pytest) 
        # não rodaram (não há evidência no stdout), então fail.
        if "test session starts" in stdout or "pytest" in stdout or "flake8" in stdout or "pylint" in stdout:
            if "failed" in stdout or "failed" in stderr:
                return False
            return True
        return False

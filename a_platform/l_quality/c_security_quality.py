class SecurityQuality:
    def evaluate(self, runtime_result_dict: dict) -> bool:
        if not runtime_result_dict:
            return False
            
        stdout = runtime_result_dict.get("stdout", "").lower()
        stderr = runtime_result_dict.get("stderr", "").lower()
        
        # Se não rodou ferramenta de segurança (bandit, safety), fail.
        if "bandit" in stdout or "safety" in stdout:
            if "issue found" in stdout or "vulnerability" in stdout:
                return False
            return True
        return False

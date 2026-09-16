class DependencyQuality:
    def evaluate(self, runtime_result_dict: dict) -> bool:
        if not runtime_result_dict:
            return False
            
        stdout = runtime_result_dict.get("stdout", "").lower()
        
        # Exige evidência de dependências checadas (pip check)
        if "pip check" in stdout or "requirements" in stdout:
            if "broken requirements" in stdout:
                return False
            return True
        return False

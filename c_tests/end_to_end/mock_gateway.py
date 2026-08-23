import json

def get_mocked_generate_function(interactive=False, repair_error=False):
    """
    Retorna uma função `generate` para ser usada como mock no LLMGateway.
    - Se interactive=True, na primeira chamada do Discovery ele retornará incompleto, e na segunda completo.
    - Se repair_error=True, o agent backend irá gerar um código com erro na primeira tentativa.
    """
    call_counts = {"discovery": 0, "repair": 0}
    
    def mock_generate(prompt: str, system_prompt: str = "", model_preference: str = "openai", **kwargs):
        system = system_prompt.lower()
        
        # 1. DISCOVERY AGENT
        if "discovery agent" in system or "analista de requisitos" in system or "discovery" in system:
            call_counts["discovery"] += 1
            if interactive and call_counts["discovery"] == 1:
                return {
                    "success": True,
                    "text": '{"is_complete": false, "missing_info_question": "Qual o domínio do projeto?", "domain": "generic", "features": [], "dataset_path": ""}'
                }
            return {
                "success": True,
                "text": '{"is_complete": true, "domain": "analytics", "features": ["etl", "reporting"], "dataset_path": "d_input/a_datasets/a_raw/vendas.csv"}'
            }
            
        # 2. ARCHITECTURE AGENT
        elif "architecture agent" in system or "decisões de arquitetura" in system:
            return {
                "success": True,
                "text": '{"components": [{"name": "etl", "type": "script", "tech": "python"}], "storage": "sqlite"}'
            }
            
        # 3. PLANNER AGENT
        elif "planner agent" in system or "planejamento" in system:
            return {
                "success": True,
                "text": '{"tasks": [{"id": "t1", "name": "ETL", "description": "Crie o ETL principal", "agent": "data", "expected_artifacts": ["main.py", "test_main.py"], "dependencies": []}], "run_commands": ["python3 main.py"]}'
            }
            
        elif "requirements.txt" in system:
            return {
                "success": True,
                "text": "pytest\npandas"
            }
            
        # 4. REPAIR LOOP
        elif "classificador de falhas" in system or "repair" in system:
            call_counts["repair"] += 1
            return {
                "success": True,
                "text": '{"file_name": "main.py", "agent_type": "backend", "fixed_content": "def run_etl():\\n  print(\\"Success ETL\\")"}'
            }
            
        # 5. SKILLS / GENERIC AGENT / CODE GENERATION
        elif "backend" in system or "dev" in system or "data engineer" in system or "skill" in system:
            if repair_error and call_counts["repair"] == 0:
                # Retorna código ruim
                code = 'def run_etl():\n  print("Syntax Error'
                test_code = 'import pytest\ndef test_etl():\n  pass'
            else:
                # Retorna código bom
                code = 'def run_etl():\n  print("Success ETL")'
                test_code = 'import pytest\ndef test_etl():\n  pass'
                
            if "test_main.py" in prompt:
                return {"success": True, "text": test_code}
            else:
                return {"success": True, "text": code}
            
        # FALLBACK
        return {
            "success": True,
            "text": '{"fallback": "mocked"}'
        }
        
    return mock_generate

import logging
import os
import subprocess
from typing import Dict, Any

from a_platform.a_core.b_domain.project_request import ProjectRequest

logger = logging.getLogger(__name__)

class RuntimeEngine:
    """
    Executa o código gerado em um ambiente físico isolado (venv)
    para provar que o projeto gerado funciona.
    """
    def __init__(self):
        pass

    def run_project(self, request: ProjectRequest) -> bool:
        domain = request.discovery_data.get("domain", "generic").lower()
        project_dir = os.path.abspath(os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id))
        
        # Limpa erros anteriores, se houver
        if "execution_error" in request.metadata:
            del request.metadata["execution_error"]
            
        if "validation_error" in request.metadata:
            del request.metadata["validation_error"]
        
        if not os.path.exists(project_dir):
            error_msg = f"Diretório do projeto não existe: {project_dir}"
            logger.error(f"[RuntimeEngine] {error_msg}")
            request.metadata["execution_error"] = error_msg
            return False
            
        logger.info(f"[RuntimeEngine] Iniciando execução isolada em {project_dir}")
        
        # 1. Setup Venv
        venv_path = os.path.join(project_dir, "venv")
        if not os.path.exists(venv_path):
            success, stdout, stderr = self._run_subprocess(f"python3 -m venv venv", cwd=project_dir, desc="Criar venv")
            if not success:
                request.metadata["execution_error"] = f"Falha ao criar venv: {stderr}"
                return False
            
        # 2. Pip Install
        req_path = os.path.join(project_dir, "requirements.txt")
        if os.path.exists(req_path):
            pip_cmd = f"./venv/bin/pip install -r requirements.txt"
            success, stdout, stderr = self._run_subprocess(pip_cmd, cwd=project_dir, desc="Instalar dependências")
            if not success:
                request.metadata["execution_error"] = f"Falha no pip install: {stderr}"
                return False
        
        # 3. Execução dos comandos definidos no Plano
        plan = request.project_plan
        if not plan or not plan.run_commands:
            logger.warning("[RuntimeEngine] Nenhum comando de execução definido no ProjectPlan.")
            request.metadata["runtime_payload"] = {
                "exit_code": 0,
                "command": None,
                "stdout": "Nenhum comando",
                "stderr": "",
                "failed_component": None
            }
            return True
            
        for cmd in plan.run_commands:
            success, stdout, stderr = self._run_subprocess(cmd, cwd=project_dir, desc=f"Executar: {cmd}")
            if not success:
                logger.error(f"[RuntimeEngine] Falha ao executar o comando de runtime: {cmd}")
                request.metadata["execution_error"] = f"Falha na execução do comando '{cmd}': {stderr}"
                request.metadata["runtime_payload"] = {
                    "exit_code": 1,
                    "command": cmd,
                    "stdout": stdout,
                    "stderr": stderr,
                    "failed_component": "runtime_command"
                }
                return False

        logger.info("[RuntimeEngine] Todos os comandos executados com sucesso (Exit Code 0).")
        request.metadata["runtime_payload"] = {
            "exit_code": 0,
            "command": "multiple",
            "stdout": "All commands succeeded",
            "stderr": "",
            "failed_component": None
        }
        return True

    def _run_subprocess(self, cmd: str, cwd: str, desc: str) -> tuple[bool, str, str]:
        logger.info(f"[RuntimeEngine] {desc}")
        try:
            result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"[RuntimeEngine] '{cmd}' falhou com código {result.returncode}")
                err_out = result.stderr.strip()
                logger.error(f"[RuntimeEngine] STDERR: {err_out}")
                return False, result.stdout.strip(), err_out
            return True, result.stdout.strip(), ""
        except Exception as e:
            logger.error(f"[RuntimeEngine] Exceção ao executar '{cmd}': {e}")
            return False, "", str(e)

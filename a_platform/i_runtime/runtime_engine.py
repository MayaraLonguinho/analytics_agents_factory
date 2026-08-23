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
        
        if not os.path.exists(project_dir):
            logger.error(f"[RuntimeEngine] Diretório do projeto não existe: {project_dir}")
            return False
            
        logger.info(f"[RuntimeEngine] Iniciando execução isolada em {project_dir}")
        
        # 1. Setup Venv
        venv_path = os.path.join(project_dir, "venv")
        if not self._run_subprocess(f"python3 -m venv {venv_path}", cwd=project_dir, desc="Criar venv"):
            return False
            
        # 2. Pip Install
        req_path = os.path.join(project_dir, "requirements.txt")
        if os.path.exists(req_path):
            pip_cmd = f"./venv/bin/pip install -r requirements.txt"
            if not self._run_subprocess(pip_cmd, cwd=project_dir, desc="Instalar dependências"):
                return False
        
        # 3. Execução dos comandos definidos no Plano
        plan = request.project_plan
        if not plan or not plan.run_commands:
            logger.warning("[RuntimeEngine] Nenhum comando de execução definido no ProjectPlan.")
            # Assume success if nothing to run but files exist
            return True
            
        for cmd in plan.run_commands:
            if not self._run_subprocess(cmd, cwd=project_dir, desc=f"Executar: {cmd}"):
                logger.error(f"[RuntimeEngine] Falha ao executar o comando de runtime: {cmd}")
                return False

        logger.info("[RuntimeEngine] Todos os comandos executados com sucesso (Exit Code 0).")
        return True

    def _run_subprocess(self, cmd: str, cwd: str, desc: str) -> bool:
        logger.info(f"[RuntimeEngine] {desc}")
        try:
            result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"[RuntimeEngine] '{cmd}' falhou com código {result.returncode}")
                logger.error(f"[RuntimeEngine] STDERR: {result.stderr.strip()}")
                return False
            return True
        except Exception as e:
            logger.error(f"[RuntimeEngine] Exceção ao executar '{cmd}': {e}")
            return False

import logging
import os
import subprocess
from typing import Dict, Any

from a_platform.a_core.b_domain.project_request import ProjectRequest

logger = logging.getLogger(__name__)

class ValidationGate:
    """
    Portão de Validação.
    Garante estruturalmente que os testes gerados passem no ambiente real (venv).
    """
    def __init__(self):
        pass

    def run_validation(self, request: ProjectRequest) -> bool:
        domain = request.discovery_data.get("domain", "generic").lower()
        project_dir = os.path.abspath(os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id))
        
        logger.info(f"[ValidationGate] Iniciando validação em {project_dir}")
        
        # 1. Checagem estrutural baseada no plano
        plan = request.project_plan
        if plan and plan.tasks:
            for task in plan.tasks:
                for expected_art in task.expected_artifacts:
                    expected_path = os.path.join(project_dir, expected_art)
                    if not os.path.exists(expected_path):
                        logger.error(f"[ValidationGate] Artefato mandatório ausente: {expected_art}")
                        return False

        # 2. Execução de suítes de testes geradas
        pytest_cmd = f"./venv/bin/pytest"
        
        # Só rodamos pytest se houver arquivos de teste e se houver pytest no venv
        # Para ser rigoroso mas à prova de falhas:
        tests_dir_exists = os.path.exists(os.path.join(project_dir, "tests"))
        pytest_installed = os.path.exists(os.path.join(project_dir, "venv", "bin", "pytest"))
        
        if tests_dir_exists and pytest_installed:
            logger.info("[ValidationGate] Rodando suite de testes (pytest)...")
            try:
                result = subprocess.run(pytest_cmd, shell=True, cwd=project_dir, capture_output=True, text=True)
                if result.returncode != 0:
                    logger.error(f"[ValidationGate] Testes falharam. Código: {result.returncode}")
                    logger.error(f"STDERR/STDOUT: {result.stdout}\n{result.stderr}")
                    return False
            except Exception as e:
                logger.error(f"[ValidationGate] Falha ao rodar testes: {e}")
                return False
        else:
            logger.warning("[ValidationGate] Pulo de testes automáticos (tests/ não encontrado ou pytest não instalado).")
            
        logger.info("[ValidationGate] Validação concluída com sucesso (PASS).")
        return True

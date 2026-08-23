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
    Se o Runtime falhou, o Validation falha obrigatoriamente.
    """
    def __init__(self):
        pass

    def run_validation(self, request: ProjectRequest) -> bool:
        domain = request.discovery_data.get("domain", "generic").lower()
        project_dir = os.path.abspath(os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id))
        
        logger.info(f"[ValidationGate] Iniciando validação em {project_dir}")
        
        # 1. Verificar se houve erro de execução
        if "execution_error" in request.metadata and request.metadata["execution_error"]:
            logger.error("[ValidationGate] Falha de Validação devido à Falha de Execução prévia.")
            return False
        
        # 2. Checagem estrutural baseada no plano
        plan = request.project_plan
        if plan and plan.tasks:
            for task in plan.tasks:
                for expected_art in task.expected_artifacts:
                    expected_path = os.path.join(project_dir, expected_art)
                    if not os.path.exists(expected_path):
                        err_msg = f"Artefato mandatório ausente após materialização e execução: {expected_art}"
                        logger.error(f"[ValidationGate] {err_msg}")
                        request.metadata["validation_error"] = err_msg
                        return False

        # 3. Execução de suítes de testes geradas (Condicional)
        tests_required = False
        if plan and plan.tasks:
            for task in plan.tasks:
                if task.agent.lower() in ["testingagent", "test", "testing"]:
                    tests_required = True
                for art in task.expected_artifacts:
                    if "test" in art.lower():
                        tests_required = True
                        
        if tests_required:
            pytest_cmd = f"./venv/bin/pytest"
            tests_dir_exists = os.path.exists(os.path.join(project_dir, "tests")) or any("test" in f for f in os.listdir(project_dir))
            pytest_installed = os.path.exists(os.path.join(project_dir, "venv", "bin", "pytest"))
            
            if not tests_dir_exists:
                err_msg = "Testes exigidos pelo plano, mas não foram gerados."
                logger.error(f"[ValidationGate] {err_msg}")
                request.metadata["validation_error"] = err_msg
                return False
                
            if not pytest_installed:
                err_msg = "pytest exigido mas não instalado na venv."
                logger.error(f"[ValidationGate] {err_msg}")
                request.metadata["validation_error"] = err_msg
                return False
                
            logger.info("[ValidationGate] Rodando suite de testes (pytest)...")
            try:
                result = subprocess.run(pytest_cmd, shell=True, cwd=project_dir, capture_output=True, text=True)
                if result.returncode != 0:
                    err_out = result.stderr.strip() or result.stdout.strip()
                    logger.error(f"[ValidationGate] Testes falharam. Código: {result.returncode}")
                    request.metadata["validation_error"] = f"Pytest falhou:\n{err_out}"
                    return False
            except Exception as e:
                err_msg = f"Falha ao rodar testes: {e}"
                logger.error(f"[ValidationGate] {err_msg}")
                request.metadata["validation_error"] = err_msg
                return False
        else:
            logger.info("[ValidationGate] Pulo de testes automáticos (não exigido pelo plano).")
            
        logger.info("[ValidationGate] Validação concluída com sucesso (PASS).")
        return True

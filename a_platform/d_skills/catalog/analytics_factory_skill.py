"""
Skill de integração do Analytics AI Factory para o Devin.

Esta skill permite que o Devin execute comandos do Analytics AI Factory
através da interface de execução disponibilizada pelo projeto.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional
import subprocess
import sys


class AnalyticsFactorySkill:
    """Skill responsável pela execução de comandos do Analytics AI Factory."""

    def __init__(self, project_root: Optional[Path | str] = None):
        self.project_root = Path(
            project_root or Path(__file__).resolve().parents[3]
        ).resolve()
        self.run_script = self.project_root / "run.py"

    def execute_command(self, command: str) -> Dict[str, Any]:
        """Executa um comando do Analytics AI Factory."""
        try:
            # Executa o comando utilizando o script principal do AAF.
            result = subprocess.run(
                [sys.executable, str(self.run_script), command],
                capture_output=True,
                text=True,
                cwd=str(self.project_root),
                timeout=60,
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "command": command,
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "O tempo limite para execução do comando foi excedido.",
                "command": command,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": command,
            }

    def get_available_commands(self) -> Dict[str, Any]:
        """Obtém os comandos disponíveis no Command Registry."""
        try:
            result = subprocess.run(
                [sys.executable, str(self.run_script), "help"],
                capture_output=True,
                text=True,
                cwd=str(self.project_root),
                timeout=30,
            )

            return {
                "success": result.returncode == 0,
                "commands": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }


def execute_analytics_factory_command(command: str) -> str:
    """
    Executa um comando do Analytics AI Factory.

    Esta função é o ponto de entrada utilizado pelo Devin para
    encaminhar comandos ao Analytics AI Factory.

    Args:
        command: Comando que será executado pelo AAF.

    Returns:
        Saída retornada pela execução do comando.
    """
    skill = AnalyticsFactorySkill()
    result = skill.execute_command(command)

    if result["success"]:
        return result["output"]

    return f"Erro: {result['error']}"


def get_analytics_factory_help() -> str:
    """
    Obtém a ajuda com os comandos disponíveis no Analytics AI Factory.

    Returns:
        Texto de ajuda retornado pelo AAF.
    """
    skill = AnalyticsFactorySkill()
    result = skill.get_available_commands()

    if result["success"]:
        return result["commands"]

    return f"Erro: {result['error']}"
"""Runtime orchestration for generated projects."""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from a_platform.a_core.d_session.b_context import ExecutionContext

@dataclass
class ExecutionResult:
    status: str = "UNKNOWN"
    exit_code: int = -1
    commands: List[str] = field(default_factory=list)
    stdout: str = ""
    stderr: str = ""
    diagnosis: str = ""
    duration: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "exit_code": self.exit_code,
            "commands": self.commands,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "diagnosis": self.diagnosis,
            "duration": self.duration,
        }


class ProjectRuntime:
    """Executes generated projects and records runtime evidence based ONLY on ProjectPlan."""

    def __init__(self, project_root: Optional[Path | str] = None):
        self.project_root = Path(project_root or Path.cwd()).resolve()

    def execute(self, request: ExecutionContext, project_path: Optional[Path | str] = None) -> ExecutionResult:
        start = time.perf_counter()
        project_dir = Path(project_path) if project_path is not None else self.project_root
        project_dir = project_dir.resolve()
        
        plan = request.project_plan
        if not plan:
            return ExecutionResult(
                status="FAILED", 
                diagnosis="Nenhum ProjectPlan fornecido. Execução abortada."
            )
            
        commands = plan.run_commands
        if not commands:
            return ExecutionResult(
                status="FAILED",
                diagnosis="Nenhum run_command estipulado no ProjectPlan. Nada a executar."
            )

        result = ExecutionResult(status="RUNNING", commands=commands)
        
        all_stdout = []
        all_stderr = []
        
        for cmd_str in commands:
            try:
                proc = subprocess.run(
                    cmd_str, 
                    shell=True,
                    cwd=str(project_dir), 
                    capture_output=True, 
                    text=True, 
                    timeout=300
                )
                
                if proc.stdout:
                    all_stdout.append(f"$ {cmd_str}\n{proc.stdout.strip()}")
                if proc.stderr:
                    all_stderr.append(f"$ {cmd_str}\n{proc.stderr.strip()}")
                    
                result.exit_code = proc.returncode
                
                if proc.returncode != 0:
                    result.status = "FAILED"
                    result.diagnosis = f"Comando falhou: {cmd_str}"
                    break
                    
            except subprocess.TimeoutExpired as exc:
                all_stderr.append(f"$ {cmd_str}\nTimeout Expired: {exc}")
                result.status = "FAILED"
                result.diagnosis = f"Timeout (300s) atingido no comando: {cmd_str}"
                break
            except Exception as exc:  # pragma: no cover
                all_stderr.append(f"$ {cmd_str}\n{exc}")
                result.status = "FAILED"
                result.diagnosis = f"Erro de execução em: {cmd_str}"
                break
        else:
            result.status = "SUCCESS"
            result.diagnosis = "Execução concluída com sucesso."

        result.stdout = "\n\n".join(all_stdout)
        result.stderr = "\n\n".join(all_stderr)
        result.duration = round(time.perf_counter() - start, 3)
        
        return result


def execute_project(request: ExecutionContext, project_path: Optional[Path | str] = None) -> ExecutionResult:
    return ProjectRuntime(project_path).execute(request, project_path=project_path)

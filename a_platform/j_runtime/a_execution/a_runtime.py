import subprocess
import time
from pathlib import Path
from typing import Optional
from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts import ExecutionResult

class ProjectRuntime:
    def execute(self, request: ExecutionContext, project_path: str) -> ExecutionResult:
        start = time.perf_counter()
        project_dir = Path(project_path).resolve()
        
        plan = getattr(request.project_context, "plan", [])
        if not plan:
            return ExecutionResult(status="FAILED", evidence="Nenhum ProjectPlan fornecido para execução.")
            
        commands = []
        for task in plan:
            commands.extend(getattr(task, "run_commands", []))
            
        if not commands:
            return ExecutionResult(status="FAILED", evidence="Nenhum comando estipulado no ProjectPlan.")
            
        all_stdout = []
        all_stderr = []
        final_exit_code = 0
        success = True
        failed_cmd = ""
        
        for cmd in commands:
            try:
                # Security: no shell=True for complex operations, but here it is a user generated command.
                proc = subprocess.run(cmd, shell=True, cwd=str(project_dir), capture_output=True, text=True, timeout=120)
                if proc.stdout: all_stdout.append(f"$ {cmd}\n{proc.stdout.strip()}")
                if proc.stderr: all_stderr.append(f"$ {cmd}\n{proc.stderr.strip()}")
                
                if proc.returncode != 0:
                    success = False
                    final_exit_code = proc.returncode
                    failed_cmd = cmd
                    break
            except Exception as exc:
                all_stderr.append(f"$ {cmd}\nException: {exc}")
                success = False
                final_exit_code = -1
                failed_cmd = cmd
                break
                
        duration = round(time.perf_counter() - start, 3)
        stdout_str = "\n\n".join(all_stdout)
        stderr_str = "\n\n".join(all_stderr)
        
        if not success:
            return ExecutionResult(
                status="FAILED",
                evidence=f"Falha ao executar comando: {failed_cmd}",
                stdout=stdout_str,
                stderr=stderr_str,
                exit_code=final_exit_code,
                duration=duration
            )
            
        return ExecutionResult(
            status="PASSED",
            evidence="Todos os comandos executados com sucesso.",
            stdout=stdout_str,
            stderr=stderr_str,
            exit_code=0,
            duration=duration
        )

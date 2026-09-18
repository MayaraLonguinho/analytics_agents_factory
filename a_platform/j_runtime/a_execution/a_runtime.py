import subprocess
import time
from pathlib import Path
from typing import Optional
from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts import ExecutionResult

from a_platform.j_runtime.b_command_policy.a_policy import CommandPolicy

class ProjectRuntime:
    def execute(self, request: ExecutionContext, project_path: str) -> ExecutionResult:
        start_time = time.perf_counter()
        project_dir = Path(project_path).resolve()
        
        plan = getattr(request.project_context, "plan", [])
        if not plan:
            return ExecutionResult(status="FAILED", evidence="Nenhum ProjectPlan fornecido para execução.")
            
        # O Planner agora adiciona comandos diretamente na task ou no run_commands.
        # Vamos agrupar os comandos das tasks que precisamos rodar.
        commands_with_task = []
        for task in plan:
            for c in task.commands:
                commands_with_task.append((task.task_id, c))
                
        # E pegar comandos globais, se existirem
        run_commands = request.metadata.get("run_commands", [])
        for c in run_commands:
            commands_with_task.append(("global", c))
            
        if not commands_with_task:
            return ExecutionResult(status="PASSED", evidence="Nenhum comando exigido pelo plano.")
            
        all_stdout = []
        all_stderr = []
        final_exit_code = 0
        success = True
        failed_cmd_str = ""
        failed_task_id = ""
        last_error = ""
        
        for task_id, raw_cmd in commands_with_task:
            valid, msg, args = CommandPolicy.parse_and_validate(raw_cmd)
            
            if not valid:
                success = False
                failed_cmd_str = raw_cmd
                failed_task_id = task_id
                last_error = msg
                all_stderr.append(f"Policy Violation na task {task_id}: {msg}")
                break
                
            try:
                # shell=False e args em lista estruturada
                proc = subprocess.run(
                    args, 
                    shell=False, 
                    cwd=str(project_dir), 
                    capture_output=True, 
                    text=True, 
                    timeout=120
                )
                if proc.stdout: all_stdout.append(f"[{task_id}] $ {raw_cmd}\n{proc.stdout.strip()}")
                if proc.stderr: all_stderr.append(f"[{task_id}] $ {raw_cmd}\n{proc.stderr.strip()}")
                
                if proc.returncode != 0:
                    success = False
                    final_exit_code = proc.returncode
                    failed_cmd_str = raw_cmd
                    failed_task_id = task_id
                    break
            except subprocess.TimeoutExpired as exc:
                all_stderr.append(f"[{task_id}] $ {raw_cmd}\nTimeoutExpired: {exc}")
                success = False
                final_exit_code = -1
                failed_cmd_str = raw_cmd
                failed_task_id = task_id
                last_error = "Timeout excedido (120s)"
                break
            except Exception as exc:
                all_stderr.append(f"[{task_id}] $ {raw_cmd}\nException: {exc}")
                success = False
                final_exit_code = -1
                failed_cmd_str = raw_cmd
                failed_task_id = task_id
                last_error = str(exc)
                break
                
        duration = round(time.perf_counter() - start_time, 3)
        stdout_str = "\n\n".join(all_stdout)
        stderr_str = "\n\n".join(all_stderr)
        
        if not success:
            return ExecutionResult(
                status="FAILED",
                evidence=f"Falha ao executar comando: {failed_cmd_str}",
                task_id=failed_task_id,
                command=[failed_cmd_str],
                working_directory=str(project_dir),
                return_code=final_exit_code,
                stdout=stdout_str,
                stderr=stderr_str,
                duration=duration,
                error=last_error
            )
            
        return ExecutionResult(
            status="PASSED",
            evidence="Todos os comandos estruturados executados com sucesso.",
            working_directory=str(project_dir),
            return_code=0,
            stdout=stdout_str,
            stderr=stderr_str,
            duration=duration
        )

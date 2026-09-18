import subprocess
import time
from pathlib import Path
from typing import List, Optional
from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts import ExecutionResult, CommandExecutionResult

from a_platform.j_runtime.b_command_policy.a_policy import CommandPolicy

COMMAND_TIMEOUT = 120.0


class ProjectRuntime:
    def execute(self, request: ExecutionContext, project_path: str) -> ExecutionResult:
        start_time = time.perf_counter()
        project_dir = Path(project_path).resolve()

        plan = getattr(request.project_context, "plan", [])
        if not plan:
            return ExecutionResult(
                status="FAILED",
                evidence="Nenhum ProjectPlan fornecido para execução.",
                duration=0.0,
            )

        # Collect all commands with their originating task_id
        commands_with_task: List[tuple] = []
        for task in plan:
            for c in task.commands:
                commands_with_task.append((task.task_id, c))

        # Global commands from metadata
        for c in request.metadata.get("run_commands", []):
            commands_with_task.append(("global", c))

        if not commands_with_task:
            return ExecutionResult(
                status="PASSED",
                evidence="Nenhum comando exigido pelo plano.",
                working_directory=str(project_dir),
                duration=0.0,
            )

        cmd_results: List[CommandExecutionResult] = []
        overall_success = True

        for task_id, raw_cmd in commands_with_task:
            cmd_start = time.perf_counter()

            # --- Policy gate ---
            valid, policy_msg, args = CommandPolicy.parse_and_validate(raw_cmd)

            if not valid:
                cr = CommandExecutionResult(
                    task_id=task_id,
                    command=[raw_cmd],
                    executable=raw_cmd.split()[0] if raw_cmd.strip() else "",
                    working_directory=str(project_dir),
                    status="DENIED",
                    policy_decision=f"DENIED: {policy_msg}",
                    error=policy_msg,
                    started_at=cmd_start,
                    finished_at=time.perf_counter(),
                    duration=round(time.perf_counter() - cmd_start, 4),
                    timeout=COMMAND_TIMEOUT,
                )
                cmd_results.append(cr)
                overall_success = False
                break  # fail-fast on policy violation

            # --- Execution ---
            try:
                proc = subprocess.run(
                    args,
                    shell=False,
                    cwd=str(project_dir),
                    capture_output=True,
                    text=True,
                    timeout=COMMAND_TIMEOUT,
                )
                cmd_end = time.perf_counter()
                success = proc.returncode == 0
                cr = CommandExecutionResult(
                    task_id=task_id,
                    command=args,
                    executable=args[0],
                    working_directory=str(project_dir),
                    status="SUCCESS" if success else "FAILED",
                    return_code=proc.returncode,
                    stdout=proc.stdout or "",
                    stderr=proc.stderr or "",
                    started_at=cmd_start,
                    finished_at=cmd_end,
                    duration=round(cmd_end - cmd_start, 4),
                    timeout=COMMAND_TIMEOUT,
                    policy_decision="ALLOWED",
                )
                cmd_results.append(cr)
                if not success:
                    overall_success = False
                    break  # fail-fast

            except subprocess.TimeoutExpired as exc:
                cmd_end = time.perf_counter()
                cr = CommandExecutionResult(
                    task_id=task_id,
                    command=args,
                    executable=args[0],
                    working_directory=str(project_dir),
                    status="TIMEOUT",
                    return_code=-1,
                    stderr=f"TimeoutExpired after {COMMAND_TIMEOUT}s",
                    started_at=cmd_start,
                    finished_at=cmd_end,
                    duration=round(cmd_end - cmd_start, 4),
                    timeout=COMMAND_TIMEOUT,
                    policy_decision="ALLOWED",
                    error=f"Timeout excedido ({COMMAND_TIMEOUT}s)",
                )
                cmd_results.append(cr)
                overall_success = False
                break

            except Exception as exc:
                cmd_end = time.perf_counter()
                cr = CommandExecutionResult(
                    task_id=task_id,
                    command=args,
                    executable=args[0] if args else raw_cmd,
                    working_directory=str(project_dir),
                    status="FAILED",
                    return_code=-1,
                    stderr=str(exc),
                    started_at=cmd_start,
                    finished_at=cmd_end,
                    duration=round(cmd_end - cmd_start, 4),
                    timeout=COMMAND_TIMEOUT,
                    policy_decision="ALLOWED",
                    error=str(exc),
                )
                cmd_results.append(cr)
                overall_success = False
                break

        total_duration = round(time.perf_counter() - start_time, 3)

        # Aggregate stdout/stderr for backward-compat consumers
        agg_stdout = "\n\n".join(
            f"[{c.task_id}] $ {' '.join(c.command)}\n{c.stdout}".strip()
            for c in cmd_results if c.stdout
        )
        agg_stderr = "\n\n".join(
            f"[{c.task_id}] $ {' '.join(c.command)}\n{c.stderr}".strip()
            for c in cmd_results if c.stderr
        )

        # Find last failing command for backward-compat fields
        last_failed = next((c for c in reversed(cmd_results) if c.status != "SUCCESS"), None)

        return ExecutionResult(
            status="PASSED" if overall_success else "FAILED",
            evidence=(
                "Todos os comandos executados com sucesso."
                if overall_success
                else f"Falha: {last_failed.error or last_failed.status} em [{last_failed.task_id}] {' '.join(last_failed.command)}"
            ),
            task_id=last_failed.task_id if last_failed else "",
            command=last_failed.command if last_failed else [],
            working_directory=str(project_dir),
            return_code=last_failed.return_code if last_failed else 0,
            stdout=agg_stdout,
            stderr=agg_stderr,
            duration=total_duration,
            error=last_failed.error if last_failed else "",
            commands=cmd_results,
        )

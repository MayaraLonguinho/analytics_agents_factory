"""
RepairLoop — evidence-based automated repair.

A repair attempt is successful ONLY when:
  1. The responsible Agent re-generates a corrected Artifact.
  2. Materialization succeeds (status == SUCCESS).
  3. Runtime re-executes the affected task commands and they PASS.
  4. ValidationGate re-validates and reports PASSED.

A lone LLM response does NOT constitute a successful repair.
"""
import logging
from dataclasses import dataclass, field
from typing import List, Optional

from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts import ExecutionResult, CommandExecutionResult

logger = logging.getLogger(__name__)


@dataclass
class RepairContext:
    """Typed evidence bundle passed to the responsible Agent for repair."""
    task_id: str
    agent_name: str
    affected_artifacts: List[str] = field(default_factory=list)
    command: List[str] = field(default_factory=list)
    return_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    validation_errors: List[str] = field(default_factory=list)
    repair_attempt: int = 1


class RepairLoop:
    def __init__(self, agent_factory, learning_engine=None):
        self.agent_factory = agent_factory
        self.learning_engine = learning_engine

    def _build_repair_context(
        self,
        runtime_result: ExecutionResult,
        task_id: str,
        agent_name: str,
        validation_errors: List[str],
        attempt: int,
    ) -> RepairContext:
        """Extract structured evidence from the failed ExecutionResult."""
        # Find the specific CommandExecutionResult that failed
        failed_cmd = next(
            (c for c in runtime_result.commands if c.status not in ("SUCCESS",) and c.task_id == task_id),
            None,
        )
        if failed_cmd is None:
            # Fallback: use aggregated data from ExecutionResult
            return RepairContext(
                task_id=task_id,
                agent_name=agent_name,
                command=runtime_result.command,
                return_code=runtime_result.return_code,
                stdout=runtime_result.stdout,
                stderr=runtime_result.stderr,
                validation_errors=validation_errors,
                repair_attempt=attempt,
            )
        return RepairContext(
            task_id=task_id,
            agent_name=agent_name,
            affected_artifacts=[],
            command=failed_cmd.command,
            return_code=failed_cmd.return_code,
            stdout=failed_cmd.stdout,
            stderr=failed_cmd.stderr,
            validation_errors=validation_errors,
            repair_attempt=attempt,
        )

    def run_repair(
        self,
        request: ExecutionContext,
        runtime_result: ExecutionResult,
        validation_errors: Optional[List[str]] = None,
        attempt: int = 1,
    ) -> bool:
        """
        Returns True only when:
          - Artifact re-generated
          - Materialization = SUCCESS
          - Runtime re-execution = PASSED
          - Validation = PASSED
        """
        if runtime_result is None or runtime_result.status == "PASSED":
            logger.info("[RepairLoop] Nenhuma falha para reparar.")
            return True

        validation_errors = validation_errors or []

        logger.warning(
            f"[RepairLoop] Iniciando tentativa {attempt}. "
            f"Task: {runtime_result.task_id}, Error: {runtime_result.error}"
        )

        # Locate the failed task in the plan
        plan = getattr(request.project_context, "plan", [])
        failed_task = next((t for t in plan if t.task_id == runtime_result.task_id), None)

        if not failed_task:
            logger.error(f"[RepairLoop] Task '{runtime_result.task_id}' não encontrada no plano.")
            return False

        agent_name = getattr(failed_task, "assigned_agent", None)
        if not agent_name:
            logger.error("[RepairLoop] A tarefa falha não possui agente designado.")
            return False

        agent = self.agent_factory.get_agent(agent_name)
        if not agent:
            logger.error(f"[RepairLoop] Agente '{agent_name}' não encontrado na Factory.")
            return False

        # Build typed repair context (structured evidence)
        repair_ctx = self._build_repair_context(
            runtime_result=runtime_result,
            task_id=runtime_result.task_id,
            agent_name=agent_name,
            validation_errors=validation_errors,
            attempt=attempt,
        )

        # Inject repair context into the prompt (structured — not replacing the context)
        original_prompt = request.prompt
        request.prompt = (
            f"[REPAIR ATTEMPT {repair_ctx.repair_attempt}] "
            f"Task '{repair_ctx.task_id}' falhou.\n"
            f"Comando: {repair_ctx.command}\n"
            f"return_code: {repair_ctx.return_code}\n"
            f"stdout: {repair_ctx.stdout[:500]}\n"
            f"stderr: {repair_ctx.stderr[:500]}\n"
            f"Erros de validação: {repair_ctx.validation_errors}\n"
            f"Corrija o código e regenere os artefatos."
        )

        try:
            # Step 1: Agent re-generates artifacts
            fixed_artifacts = agent.execute_task(failed_task, request)
            request.prompt = original_prompt

            if not fixed_artifacts:
                logger.error("[RepairLoop] Agente não retornou artefatos corrigidos.")
                return False

            # Step 2: Re-materialize
            from a_platform.h_materializer.a_materializer import ArtifactMaterializer
            from a_platform.f_mcps.d_registry.b_executor import MCPExecutor
            materializer = ArtifactMaterializer(MCPExecutor())
            mat_res = materializer.materialize(request, fixed_artifacts)

            if mat_res.status != "SUCCESS":
                logger.error(f"[RepairLoop] Materialização do reparo falhou: {mat_res.evidence}")
                return False

            # Step 3: Re-execute via Runtime
            from a_platform.j_runtime.a_execution.a_runtime import ProjectRuntime
            project_path = getattr(request.project_context, "project_path", "")
            new_runtime_result = ProjectRuntime().execute(request, project_path)

            if new_runtime_result.status != "PASSED":
                logger.error(
                    f"[RepairLoop] Re-execução falhou após reparo: {new_runtime_result.error}"
                )
                return False

            # Step 4: Re-validate
            from a_platform.k_validation.a_validation_gate import ValidationGate
            new_val_result = ValidationGate().evaluate(request, new_runtime_result)

            if new_val_result.status != "PASSED":
                logger.error(
                    f"[RepairLoop] Revalidação falhou após reparo: {new_val_result.evidence}"
                )
                return False

            logger.info("[RepairLoop] Reparo concluído com sucesso. Todos os gates passaram.")
            return True

        except Exception as exc:
            logger.error(f"[RepairLoop] Exceção durante o reparo: {exc}")
            request.prompt = original_prompt
            return False

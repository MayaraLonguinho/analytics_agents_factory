import logging
from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts import ExecutionResult, ValidationResult
from .b_structure_validation import StructureValidation
from .c_execution_validation import ExecutionValidation
from .d_project_validation import ProjectValidation

logger = logging.getLogger(__name__)


class ValidationGate:
    def __init__(self):
        self.struct_val = StructureValidation()
        self.exec_val = ExecutionValidation()
        self.proj_val = ProjectValidation()

    def evaluate(self, request: ExecutionContext, runtime_result: ExecutionResult) -> ValidationResult:
        if runtime_result is None:
            return ValidationResult(status="FAILED", evidence="Nenhum resultado de runtime fornecido.")

        if not self.proj_val.validate(request):
            return ValidationResult(
                status="FAILED",
                evidence="Falha na validação de metadados do projeto (project_id, plan, project_path, materialization_status).",
            )

        if not self.struct_val.validate(request):
            return ValidationResult(
                status="FAILED",
                evidence="Falha na validação de estrutura: artefatos ausentes ou inválidos no disco.",
            )

        if not self.exec_val.validate(runtime_result):
            return ValidationResult(
                status="FAILED",
                evidence=(
                    f"Falha na validação de execução: "
                    f"status={runtime_result.status}, return_code={runtime_result.return_code}."
                ),
            )

        return ValidationResult(status="PASSED", evidence="Todas as validações concluídas com sucesso.")

import os
from a_platform.b_contracts.e_execution_context import ExecutionContext

class StructureValidation:
    def validate(self, request: ExecutionContext) -> bool:
        project_dir = getattr(request.project_context, "project_path", "")
        if not project_dir or not os.path.exists(project_dir):
            return False
            
        # Verifica presença de arquivos obrigatórios mínimos definidos pelo plano
        plan = getattr(request.project_context, "plan", [])
        for task in plan:
            for expected_art in getattr(task, "expected_artifacts", []):
                if not os.path.exists(os.path.join(project_dir, expected_art)):
                    return False
        return True

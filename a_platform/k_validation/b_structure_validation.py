import os
import py_compile
from a_platform.b_contracts.e_execution_context import ExecutionContext

class StructureValidation:
    def validate(self, request: ExecutionContext) -> bool:
        project_dir = getattr(request.project_context, "project_path", "")
        if not project_dir or not os.path.exists(project_dir):
            return False
            
        plan = getattr(request.project_context, "plan", [])
        for task in plan:
            for expected_art in getattr(task, "expected_artifacts", []):
                full_path = os.path.join(project_dir, expected_art)
                
                # Integridade do caminho
                if not os.path.abspath(full_path).startswith(os.path.abspath(project_dir)):
                    return False
                
                # Existência
                if not os.path.exists(full_path):
                    return False
                    
                # Conteúdo não vazio
                if os.path.getsize(full_path) == 0:
                    # Permite vazio se for __init__.py, senao falha
                    if not full_path.endswith("__init__.py"):
                        return False
                
                # Compilação estática sem executar
                if full_path.endswith(".py"):
                    try:
                        py_compile.compile(full_path, doraise=True)
                    except py_compile.PyCompileError:
                        return False

        return True
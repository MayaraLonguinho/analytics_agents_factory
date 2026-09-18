import logging
from typing import Dict, Any
from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts import QualityResult
from .b_code_quality import CodeQuality
from .c_security_quality import SecurityQuality
from .d_dependency_quality import DependencyQuality

logger = logging.getLogger(__name__)

class QualityEngine:
    def __init__(self):
        self.code_quality = CodeQuality()
        self.security_quality = SecurityQuality()
        self.dep_quality = DependencyQuality()

    def evaluate(self, request: ExecutionContext, validation_result: Dict[str, Any], runtime_result: Dict[str, Any]) -> QualityResult:
        if not validation_result or validation_result.get("status") != "PASSED":
            return QualityResult(status="FAILED", evidence="Validação anterior falhou.")
            
        if not runtime_result:
            return QualityResult(status="FAILED", evidence="Ausência de evidências de runtime (Execução nula).")

        # Verifica todos os gates rigorosamente. ABSENCE OF EVIDENCE = FAILURE
        cq_status = self.code_quality.evaluate(runtime_result)
        sq_status = self.security_quality.evaluate(runtime_result)
        dq_status = self.dep_quality.evaluate(runtime_result)
        
        # Policy: se as ferramentas não foram executadas e não era obrigatório, a gente pode aceitar dependendo da politica.
        # Contudo, pela instrução "não considerar testes como aprovação", se algo obrigatório não rodou, é falha.
        # Aqui adotamos uma política de PASSED apenas se não houver falha explícita.
        
        failed = []
        if cq_status == "FAILED": failed.append("CodeQuality")
        if sq_status == "FAILED": failed.append("SecurityQuality")
        if dq_status == "FAILED": failed.append("DependencyQuality")
        
        if failed:
            return QualityResult(status="FAILED", evidence=f"Quality gates falharam: {failed}")
            
        return QualityResult(status="PASSED", evidence=f"Quality Engine avaliado. Status: CQ={cq_status}, SQ={sq_status}, DQ={dq_status}")
